"""A simple bot that buys a card when it can."""

from src.game import agent
from src.game import gem_utils
from src.game import player_game_state
from src.proto.deck_proto import Deck
from src.proto.gem_proto import GemType
from src.proto.player_action_proto import PlayerAction


class GreedyBuyBot(agent.Agent):
  """An agent that greedily buys bot."""
  def PlayTurn(self, player_game_state):
    card_to_buy = None
    for deck in [Deck.LEVEL_3, Deck.LEVEL_2, Deck.LEVEL_1]:
      for card in player_game_state.revealed_cards[deck]:
        if player_game_state.CanPurchaseCard(card):
          card_to_buy = card
    if card_to_buy is None:
      available_gems = player_game_state.gem_counts
      available_gem_types = gem_utils.GetNonEmptyGemTypes(available_gems)
      if GemType.GOLD in available_gem_types:
        available_gem_types.remove(GemType.GOLD)
      if (len(available_gem_types) == 1 and
          player_game_state.CanTakeTwo(available_gem_types[0]) and
          player_game_state.GemLimit() > 1):
        action = agent.TakeGems({available_gem_types[0]: 2})
      else:
        num_to_take = min(3, player_game_state.GemLimit())
        action = agent.TakeGems(
            {gem_type: 1 for gem_type in available_gem_types[:num_to_take]})
    else:
      action = agent.BuyCard(player_game_state, card_to_buy)
    claimable_nobles = player_game_state.GetClaimableNobles()
    if len(claimable_nobles) > 0:
      action = action._replace(noble_tile_id=claimable_nobles[0].asset_id)
    return action
