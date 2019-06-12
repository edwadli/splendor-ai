"""A bot that reserves high-value cards."""

import collections
import logging
import math

from src.game import agent
from src.game import gem_utils
from src.game import player_game_state as game_state_utils
from src.proto.gem_proto import GemType


_MINIMUM_CARD_VALUE = 0.85
_MINIMUM_SECONDARY_CARD_VALUE = 2.0
_RERANK_CUTOFF = 3
_MOST_NEEDED_GEM_DOUBLE_TAKE_MINIMUM = 2


def CanPossiblyAfford(card, state):
  discounted_cost = gem_utils.GetDiscountedCost(
      card.cost, state.self_state.gem_discounts)
  return 10 >= gem_utils.NumGems(discounted_cost)


class ValueBuyBot(agent.Agent):
  """An agent that tries to prioritize high value cards."""
  def PlayTurn(self, player_game_state):
    card_path = self._GetNextPurchaseTarget(player_game_state)
    action = self._GetActionTowardsPurchase(card_path, player_game_state)
    # Claim any noble if possible.
    claimable_nobles = player_game_state.GetClaimableNobles()
    if len(claimable_nobles) > 0:
      action = action._replace(noble_tile_id=claimable_nobles[0].asset_id)
    return action

  def _GetNextPurchaseTarget(self, state):
    card_paths = self._GetTopCardPaths(state)
    card_paths = self._RerankCardPaths(state, card_paths)
    if len(card_paths) == 0:
      raise ValueError("No card paths targeted")
    return card_paths[0]

  def _GetTopCardPaths(self, state):
    card_table = {}  # asset_id to card, for convenience
    card_values = {}  # asset_id to card value
    card_discount = collections.defaultdict(list)  # gem discount to card
    for cards in state.revealed_cards.values():
      for card in cards:
        card_table[card.asset_id] = card
        card_values[card.asset_id] = self._GetSelfCardValue(
            card, state)
        card_discount[card.gem].append(card.asset_id)
    for card in state.self_state.reserved_cards:
      card_table[card.asset_id] = card
      card_values[card.asset_id] = self._GetSelfCardValue(
          card, state)
      card_discount[card.gem].append(card.asset_id)

    # Sort cards by value.
    top_values = sorted(
        card_values.keys(), key=lambda k: card_values[k], reverse=True)
    # Get the highest value ancestor card that can possibly be
    # afforded with current discounts.
    card_paths = []
    for asset_id in top_values:
      card = card_table[asset_id]
      gem_types_needed = gem_utils.GetNonEmptyGemTypes(card.cost)
      ancestor_cards = []
      for gem_type in gem_types_needed:
        for ancestor_asset_id in card_discount[gem_type]:
          if ancestor_asset_id == asset_id:
            continue
          ancestor_card = card_table[ancestor_asset_id]
          if not CanPossiblyAfford(ancestor_card, state):
            continue
          ancestor_cards.append(card_table[ancestor_asset_id])
      if len(ancestor_cards) == 0:
        if CanPossiblyAfford(card, state):
          card_paths.append([card])
        continue
      max_ancestor_value = max(
          card_values[c.asset_id] for c in ancestor_cards)
      ancestor_cards = filter(
          lambda c: card_values[c.asset_id] == max_ancestor_value,
          ancestor_cards)
      for ancestor_card in ancestor_cards:
        card_paths.append([ancestor_card, card])
    return card_paths

  def _LogCardPaths(self, state, card_paths):
    msg_data = []
    for cp in card_paths:
      cp_ids = [] 
      msg_data.append(cp_ids)
      for c in cp:
        cp_ids.append(c.asset_id + ": " +
                      str(self._GetSelfCardValue(c, state)))
    logging.debug("Card paths: " + str(msg_data))
    if len(cp) > 0:
      logging.debug(
          "Best card tempo: " +
          str(self._GetTempoForCard(cp[0], state, state.self_state)))

  def _RerankCardPaths(self, state, card_paths):
    reranked_card_paths = card_paths
    for card_path in reranked_card_paths:
      if len(card_path) == 0:
        raise ValueError("Found empty card path")
    # Weakly prefer reserved cards (tie breaker).
    reranked_card_paths.sort(
        key=lambda cp: state.GetReservedCardById(cp[0].asset_id) is None)
    # Prefer card paths that can be bought faster.
    card_tempos = {
        cp[0].asset_id: self._GetTempoForCard(cp[0], state, state.self_state)
        for cp in reranked_card_paths}
    reranked_card_paths.sort(key=lambda cp: card_tempos[cp[0].asset_id])
    # Strongly prefer cards that will make you win upon purchase
    # (move them to the front).
    reranked_card_paths.sort(key=lambda cp: 
        (state.self_state.num_points + cp[0].points) < 15)
    # Only consider the fastest card paths.
    reranked_card_paths = reranked_card_paths[:_RERANK_CUTOFF]
    # Maximize total card_path value.
    reranked_card_paths.sort(key=lambda cp: sum(
        self._GetSelfCardValue(c, state) for c in cp), reverse=True)

    self._LogCardPaths(state, reranked_card_paths)
  
    return reranked_card_paths

  def _GetActionTowardsPurchase(self, card_path, state):
    if len(card_path) == 0:
      raise ValueError("Card path is empty")
    card = card_path[0]
    # Try to purchase the card.
    if state.CanPurchaseCard(card):
      return agent.BuyCard(state, card)
    # Check if we should reserve the card instead.
    card_value = self._GetSelfCardValue(card, state)
    if (state.CanReserve() and card_value >= _MINIMUM_CARD_VALUE and
        state.GetReservedCardById(card.asset_id) is None):
      for opponent_state in state.opponent_states:
        opp_card_value = self._GetOppCardValue(card, state, opponent_state)
        if opp_card_value >= card_value:
          return self._ReserveCardAndTakeGold(state, card)
    # Take gems to get to the card next time.
    if len(card_path) > 1:
      secondary_card=card_path[1]
      # Reserve secondary card if high value and gives gold.
      card_value = self._GetSelfCardValue(
          secondary_card, state)
      if (state.CanReserve() and
          state.gem_counts[GemType.GOLD] > 0 and
          card_value >= _MINIMUM_SECONDARY_CARD_VALUE and
          state.GetReservedCardById(secondary_card.asset_id) is None):
        return self._ReserveCardAndTakeGold(state, secondary_card,
                                            cost_card=card)
      # Otherwise just get gems.
      action = self._GetGemActionTowardsCard(
          state, card, secondary_card=secondary_card)
    else:
      action = self._GetGemActionTowardsCard(state, card)
    return action

  def _ReserveCardAndTakeGold(self, state, card, cost_card=None):
    if cost_card is None:
      cost_card = card
    reserve_action = agent.ReserveCardAndTakeGold(state, card)
    gem_action = self._TakeGemsAndReturnUnnecessary(
        state, cost_card, reserve_action.gems_taken,
        state.self_state.gem_counts)
    return gem_action._replace(
        reserved_card_id=reserve_action.reserved_card_id)

  def _GetTempoForCard(self, card, state, self_state):
    """Estimates the number of rounds it would take to purchase 'card'."""
    discounted_cost = gem_utils.GetDiscountedCost(
        card.cost, self_state.gem_discounts)
    discounted_cost = gem_utils.GetDiscountedCost(
        discounted_cost, self_state.gem_counts)
    if len(discounted_cost) == 0:
      return 1.0
    tempo_cost = float(max(discounted_cost.values())) * 2.0/3.0 + 1.0
    # Add penalty if needed gems can't be taken that round.
    gems_wanted = gem_utils.GetNonEmptyGemTypes(
        self._GetMissingGemsForCard(card, state))
    num_missing = 0
    for gem_wanted in gems_wanted:
      if state.gem_counts[gem_wanted] == 0:
        num_missing += 1
    if len(gems_wanted) <= 3 and num_missing > 0:
      tempo_cost += num_missing
    elif len(gems_wanted) > 3 and len(gems_wanted) - num_missing < 3:
      tempo_cost += 3
    return tempo_cost

  def _GetSelfCardValue(self, card, state, self_state=None):
    if self_state is None:
      self_state = state.self_state
    point_benefit = card.points + 0.15  # add estimated discount benefit
    tempo_cost = self._GetTempoForCard(card, state, self_state)
    points_per_cost = point_benefit/tempo_cost
    return points_per_cost

  def _GetOppCardValue(self, card, state, opp_state):
    return self._GetSelfCardValue(card, state, self_state=opp_state)

  def _GetMissingGemsForCard(self, card, state):
    discounted_cost = gem_utils.GetDiscountedCost(
        card.cost, state.self_state.gem_discounts)
    gems_needed = gem_utils.GetDiscountedCost(
        discounted_cost, state.self_state.gem_counts)
    return gems_needed

  def _GetGemsByScarcity(self, gems_set, available_gems, omit_unavailable=True):
    gems_by_scaricty = {
        gem: available_gems[gem] for gem in gems_set
        if not omit_unavailable or (omit_unavailable and
                                    available_gems[gem] > 0)}
    return gem_utils.GemsByCount(gems_by_scaricty)

  def _TakeGemsAndReturnUnnecessary(
      self, state, card, gems_to_take, gems_owned):
    num_to_return = gem_utils.NumGems(gems_to_take) - state.GemLimit()
    if num_to_return <= 0:
      return agent.TakeGems(gems_to_take)

    gems_needed = gem_utils.GetDiscountedCost(
        card.cost, state.self_state.gem_discounts)

    total_gems = (collections.Counter(gems_owned) +
                  collections.Counter(gems_to_take))
    unnecessary_gems = collections.Counter()
    for gem, count in total_gems.iteritems():
      if gem == GemType.GOLD:
        continue  # never return gold
      unnecessary_count = count - gems_needed[gem]
      if unnecessary_count > 0:
        unnecessary_gems[gem] = unnecessary_count
    if gem_utils.AllZerosExcept(gems_to_take, GemType.GOLD):
      unnecessary_gems = total_gems
      del unnecessary_gems[GemType.GOLD]

    # Give back by least scarce.
    gold_buffer = gems_owned[GemType.GOLD]
    gems_to_return = collections.Counter()
    for _ in range(num_to_return):
      returnable_gem_types = gem_utils.GetNonEmptyGemTypes(unnecessary_gems)
      if len(returnable_gem_types) == 0 and gold_buffer > 0:
        gold_buffer -= 1
        returnable_gem_types = gem_utils.GetNonEmptyGemTypes(total_gems)
      gem_priority_list = self._GetGemsByScarcity(
          returnable_gem_types,
          collections.Counter(state.gem_counts) + gems_to_return,
          omit_unavailable=False)
      gem_priority_list.reverse()
      if len(gem_priority_list) == 0:
        logging.error("Targeting: " + str(gems_needed))
        logging.error("Available spots: " + str(state.GemLimit()))
        logging.error("Gems owned: " + str(gems_owned))
        logging.error("Gems taken: " + str(gems_to_take))
        raise ValueError("All gems needed, but too many taken.")
      gem_to_return = gem_priority_list[0]
      gems_to_return[gem_to_return] += 1
      unnecessary_gems[gem_to_return] -= 1
      total_gems[gem_to_return] -= 1

    # Simplify taking + returning of the same gem.
    gems_to_take = collections.Counter(gems_to_take)
    common_gem_count = gems_to_take & gems_to_return
    gems_to_take -= common_gem_count
    gems_to_return -= common_gem_count
    return agent.TakeGems(gems_to_take, returned=gems_to_return)

  def _GetMostNeededGem(self, gems):
    most_needed_gems = gem_utils.GetMaxCountGems(gems)
    if len(most_needed_gems) == 0:
      raise ValueError("Should have bought a card")
    return most_needed_gems[0]

  def _GetGemActionTowardsCard(self, state, card, secondary_card=None):
    if state.CanPurchaseCard(card):
      raise ValueError("Should have purchased card")
    gems = self._GetMissingGemsForCard(card, state)
    if len(gems) == 0:
      raise ValueError("Can't purchase card but no missing gems")
    if secondary_card is not None:
      secondary_gems = gem_utils.GetDiscountedCost(
          secondary_card.cost, state.self_state.gem_discounts)
    else:
      secondary_gems = None
    if gems[GemType.GOLD] > 0:
      raise ValueError("Should not need gold gems")
    num_to_take = 3

    # Take two of the most needed gem if possible.
    most_needed_gem = self._GetMostNeededGem(gems)
    if (state.CanTakeTwo(most_needed_gem) and
        gems[most_needed_gem] >= _MOST_NEEDED_GEM_DOUBLE_TAKE_MINIMUM
        and num_to_take > 1):
      return self._TakeGemsAndReturnUnnecessary(
          state, card, {most_needed_gem: 2}, state.self_state.gem_counts)

    # Otherwise, take one of each, starting with the scarcest.
    gem_priority_list = self._GetGemsByScarcity(
        gem_utils.GetNonEmptyGemTypes(gems), state.gem_counts)
    gems_to_take = collections.Counter(
        gem_utils.CountGems(gem_priority_list[:num_to_take]))
    num_to_take -= len(gems_to_take)
    if num_to_take == 0:
      return self._TakeGemsAndReturnUnnecessary(
          state, card, gems_to_take, state.self_state.gem_counts)

    # Try to double take secondary gems if possible.
    if (len(gems_to_take) == 0 and secondary_gems is not None and
        not state.CanPurchaseCard(secondary_card)):
      most_needed_gem = self._GetMostNeededGem(secondary_gems)
      if (state.CanTakeTwo(most_needed_gem) and
          secondary_gems[most_needed_gem] >= _MOST_NEEDED_GEM_DOUBLE_TAKE_MINIMUM
          and num_to_take > 1):
        return self._TakeGemsAndReturnUnnecessary(
            state, card, {most_needed_gem: 2}, state.self_state.gem_counts)

    # Take secondary gems if there is room after > 1 primary gems taken.
    if secondary_gems is not None:
      for gem in gems_to_take:
        del secondary_gems[gem]  # remove option of already-taken gem
      gem_priority_list = self._GetGemsByScarcity(
          gem_utils.GetNonEmptyGemTypes(secondary_gems), state.gem_counts)
      secondary_gems_to_take = collections.Counter(
          gem_utils.CountGems(gem_priority_list[:num_to_take]))
      num_to_take -= len(secondary_gems_to_take)
      gems_to_take += secondary_gems_to_take
      if num_to_take == 0:
        return self._TakeGemsAndReturnUnnecessary(
            state, card, gems_to_take, state.self_state.gem_counts)

    # Take arbitrary gems starting with the scarcest.
    possible_gems_to_take = [
        gem for gem in state.gem_counts
        if gem not in gems_to_take and gem != GemType.GOLD]
    gem_priority_list = self._GetGemsByScarcity(
        possible_gems_to_take, state.gem_counts)
    gems_to_take += collections.Counter(
        gem_utils.CountGems(gem_priority_list[:num_to_take]))
    return self._TakeGemsAndReturnUnnecessary(
        state, card, gems_to_take, state.self_state.gem_counts)
