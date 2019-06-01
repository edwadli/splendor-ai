"""Interface for agents and wrapper around PlayerState."""

import abc
import collections

from src.game import gem_utils
from src.proto.gem_proto import GemType


class Player(object):
	"""Abstract wrapper around PlayerState for agents to subclass."""
	__metaclass__ = abc.ABCMeta

	def __init__(self, player_state):
		"""Precomputes relevant values of player_state."""
		self._player_state = player_state
		self._gem_counts = gem_utils.CountGems(player_state.gems)
		self._unhidden_reserved_cards = player_state.unhidden_reserved_cards
		self._hidden_reserved_cards = player_state.hidden_reserved_cards
		
		# Derived values from a player's purchased cards and nobles.
		self._num_points = 0
		self._gem_discounts = collections.defaultdict(int)  # keyed by GemType
		for card in player_state.purchased_cards:
			self._num_points += card.points
			self._gem_discounts[card.gem.type] += 1
		for noble_tile in player_state.noble_tiles:
			self._num_points += noble_tile.points

	@abc.abstractmethod
	def PlayTurn(self, player_game_state):
		"""Returns a PlayerAction given the PlayerGameState."""
		raise NotImplementedError("No implementation for PlayTurn method.")

	@property
	def player_state(self):
		return self._player_state

	@property
	def gem_counts(self):
		return self._gem_counts
	
	@property
	def unhidden_reserved_cards(self):
		return self._unhidden_reserved_cards

	@property
	def hidden_reserved_cards(self):
		return self._hidden_reserved_cards
	
	@property
	def reserved_cards(self):
		return self._unhidden_reserved_cards + self._hidden_reserved_cards
	
	@property
	def num_purchased_cards(self):
		return len(self.player_state.purchased_cards)
	
	@property
	def num_reserved_cards(self):
		return len(self.reserved_cards)

	@property
	def num_points(self):
		return self._num_points
	
	@property
	def gem_discounts(self):
		return self._gem_discounts
	
