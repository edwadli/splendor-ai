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
