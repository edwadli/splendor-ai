"""Interface for agents."""

import abc
import collections

from src.game import gem_utils
from src.proto.gem_proto import GemType
from src.proto.player_action_proto import PlayerAction


class Agent(object):
  """Base abstract class for agents."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def PlayTurn(self, player_game_state):
    """Returns a PlayerAction given the PlayerGameState."""
    raise NotImplementedError("No implementation for PlayTurn method.")


def BuyCard(player_game_state, card):
  discounted_cost = gem_utils.GetDiscountedCost(
      card.cost, player_game_state.self_state.gem_discounts)
  # print "CARD: " + str(card)
  # print "DISCOUNTED COST: " + str(discounted_cost)
  self_gems = player_game_state.self_state.gem_counts
  gem_diff = collections.Counter(discounted_cost) - collections.Counter(self_gems)
  num_gold_needed = sum(gem_diff.values())
  gems_returned = collections.Counter({GemType.GOLD: num_gold_needed})
  for gem_type, count in discounted_cost.iteritems():
    gems_returned[gem_type] = min(self_gems[gem_type], count)
  # print "GEMS RETURNED: " + str(gems_returned)
  return PlayerAction(
      gems_taken=collections.Counter(),
      gems_returned=gems_returned,
      purchased_card_id=card.asset_id,
      reserved_card_id=None,
      topdeck_level=None,
      noble_tile_id=None)


def TakeGems(gems):
  return PlayerAction(
      gems_taken=collections.Counter(gems),
      gems_returned=collections.Counter(),
      purchased_card_id=None,
      reserved_card_id=None,
      topdeck_level=None,
      noble_tile_id=None)


# class PlayerActionBuilder(object):
#     """Wrapper for building a PlayerAction."""
#     def __init__(self):
#       self._gems_taken = collections.Counter()
#       self._gems_returned = collections.Counter()
#       self._purchased_card_id = None
#       self._reserved_card_id = None
#       self._topdeck_level = None
#       self._noble_tile_id = None

#     def TakeGem(self, gem_type):
#       self._gems_taken[gem_type] += 1

#     def TakeGems(self, gems):
#       self._gems_taken += collections.Counter(gems)

#     def ReturnGem(self, gem_type):
#       self._gems_returned[gem_type] += 1

#     def ReturnGems(self, gems):
#       self._gems_returned += collections.Counter(gems)

#     def PurchaseCard(self, asset_id, payment=None):
#       self._purchased_card_id = asset_id
#       if payment is not None:
#         self.ReturnGems(payment)

#     def ReserveCard(self, asset_id, take_gold=False):
#       self._reserved_card_id = asset_id
#       if take_gold:
#         self.TakeGem(GemType.GOLD)

#     def TopDeck(self, deck, take_gold=False):
#       self._topdeck_level = deck
#       if take_gold:
#         self.TakeGem(GemType.GOLD)

#     def ClaimNoble(self, asset_id):
#       self._noble_tile_id = asset_id
