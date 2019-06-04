"""Interface for agents."""

import abc
import collections

from src.proto.gem_proto import GemType


class Agent(object):
  """Base abstract class for agents."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def PlayTurn(self, player_game_state):
    """Returns a PlayerAction given the PlayerGameState."""
    raise NotImplementedError("No implementation for PlayTurn method.")


class PlayerActionBuilder(object):
    """Wrapper for building a PlayerAction."""
    def __init__(self):
      self._gems_taken = collections.Counter()
      self._gems_returned = collections.Counter()
      self._purchased_card_id = None
      self._reserved_card_id = None
      self._topdeck_level = None
      self._noble_tile_id = None

    def TakeGem(self, gem_type):
      self._gems_taken[gem_type] += 1

    def TakeGems(self, gems):
      self._gems_taken += collections.Counter(gems)

    def ReturnGem(self, gem_type):
      self._gems_returned[gem_type] += 1

    def ReturnGems(self, gems):
      self._gems_returned += collections.Counter(gems)

    def PurchaseCard(self, asset_id, payment=None):
      self._purchased_card_id = asset_id
      if payment is not None:
        self.ReturnGems(payment)

    def ReserveCard(self, asset_id, take_gold=False):
      self._reserved_card_id = asset_id
      if take_gold:
        self.TakeGem(GemType.GOLD)

    def TopDeck(self, deck, take_gold=False):
      self._topdeck_level = deck
      if take_gold:
        self.TakeGem(GemType.GOLD)

    def ClaimNoble(self, asset_id):
      self._noble_tile_id = asset_id
