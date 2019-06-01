"""Interface for viewing the field (game board)."""

import collections

from src.game import gem_utils
from src.game import player
from src.proto.game_state_proto import Deck


def GetRevealedCards(game_state, game_rules):
	"""Returns a dict from Deck to list of revealed development cards."""
	revealed_cards = collections.defaultdict(list)
	cards_per_level = game_rules.num_cards_revealed_per_level
	for deck, cards in game_state.development_cards:
		revealed_cards[deck] = cards[-cards_per_level:]
	return revealed_cards


class OpponentState(player.Player):
	"""Wrapper for PlayerState as it would appear to an opponent."""
	def __getattribute__(self, attr):
		private_attributes = [
			"player_state",
			"hidden_reserved_cards",
		]
		if attr in private_attributes:
			raise AttributeError
		return object.__getattribute__(self, attr)

	@property
	def num_hidden_reserved_cards(self):
		return self.num_reserved_cards - len(self.unhidden_reserved_cards)
	

class PlayerGameState(object):
	"""Wrapper for exposing GameState according to GameRules."""
	def __init__(self, game_state, game_rules):
		"""Precomputes relevant values of game_state."""
		self._game_state = game_state
		self._game_rules = game_rules
		self._gem_counts = gem_utils.CountGems(game_state.available_gems)
		self._revealed_cards = GetRevealedCards(game_state, game_rules)
		# The order of 'self._opponent_states' respects the turn
		# ordering, starting with the next player's state.
		self._opponent_states = []
		num_opponents = len(game_state.player_states) - 1
		for i in range(num_opponents):
			opponent_idx = (i + turn + 1) % num_players
			self._opponent_states.append(OpponentState(
				game_state.player_states[opponent_idx]))

	def CanTakeTwo(self, gem_type):
		"""Returns whether the player can take two of the gem type.
		
		Note this does not check whether the player can take more gems.

		Params:
			gem_type: the desired GemType.

		Returns:
			A boolean for whether double-taking is valid.
		"""
		return (self.gem_counts[gem_type] >=
			self._game_rules.min_double_take_gems)

	def CanTopDeck(self, deck):
		"""Returns whether there are any cards left in the given deck."""
		num_cards = len(self._game_state.development_cards[deck])
		num_cards_revealed = len(self.revealed_cards[deck])
		num_cards_left = num_cards - num_cards_revealed
		return num_cards_left > 0

	@property
	def gem_counts(self):
		return self._gem_counts

	@property
	def revealed_cards(self):
		return self._revealed_cards

	@property
	def opponent_states(self):
		return self._opponent_states
	
