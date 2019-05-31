"""Interface for agents and wrapper around PlayerState."""

import abc
from src.proto.development_card_proto import GemType

class Player(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self, player_state):
		"""Precomputes relevant values of player_state."""
		self._player_state = player_state
		self._gold_gems = player_state.num_gold_gems
		self._blue_gems = player_state.num_blue_gems
		self._green_gems = player_state.num_green_gems
		self._red_gems = player_state.num_red_gems
		self._brown_gems = player_state.num_brown_gems
		self._white_gems = player_state.num_white_gems
		self._reserved_cards = player_state.reserved_cards
		self._hidden_reserved_cards = player_state.hidden_reserved_cards
		
		# Derived values
		self._num_purchased_cards = len(player_state.purchased_cards)
		self._num_reserved_cards = (
			len(self._reserved_cards) + len(self._hidden_reserved_cards))
		self._num_points = 0
		self._blue_discounts = 0
		self._green_discounts = 0
		self._red_discounts = 0
		self._brown_discounts = 0
		self._white_discounts = 0
		for card in player_state.purchased_cards:
			self._num_points += card.points
			if card.gem == GemType.BLUE:
				self._blue_discounts += 1
			elif card.gem == GemType.GREEN:
				self._green_discounts += 1
			elif card.gem == GemType.RED:
				self._red_discounts += 1
			elif card.gem == GemType.WHITE:
				self._white_discounts += 1
			elif card.gem == GemType.BROWN:
				self._brown_discounts += 1
			else:
				raise ValueError("GemType unhandled.")

	@abc.abstractmethod
	def PlayTurn(gamestate):
		"""Returns a PlayerAction given the 'gamestate'."""
		raise NotImplementedError("No implementation for PlayTurn method.")

	@property
	def player_state(self):
		return self._player_state

	@property
	def gold_gems(self):
		return self._gold_gems
	
	@property
	def blue_gems(self):
		return self._blue_gems
	
	@property
	def green_gems(self):
		return self._green_gems
	
	@property
	def red_gems(self):
		return self._red_gems
	
	@property
	def brown_gems(self):
		return self._brown_gems
	
	@property
	def white_gems(self):
		return self._white_gems

	@property
	def reserved_cards(self):
		return self._reserved_cards
		
	@property
	def hidden_reserved_cards(self):
		return self._hidden_reserved_cards
	
	@property
	def num_purchased_cards(self):
		return self._num_purchased_cards
	
	@property
	def num_reserved_cards(self):
		return self._num_reserved_cards

	@property
	def num_points(self):
		return self._num_points
	
	@property
	def blue_discounts(self):
		return self._blue_discounts

	@property
	def green_discounts(self):
		return self._green_discounts

	@property
	def red_discounts(self):
		return self._red_discounts

	@property
	def brown_discounts(self):
		return self._brown_discounts

	@property
	def white_discounts(self):
		return self._white_discounts

