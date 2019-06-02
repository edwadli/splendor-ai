"""Interface for viewing the field (game board)."""

import collections

from src.game import gem_utils
from src.game import player
from src.proto.deck_proto import Deck


def GetRevealedCards(development_cards_dict, game_rules):
	"""Returns a dict from Deck to list of revealed development cards.

	The last N cards from each list are considered revealed cards. All
	other cards are considered still part of the unrevealed decks.

	Params:
		development_cards_dict: Dict from Deck to list of
			DevelopmentCards. Assumes all the cards in each list are
			of the same level (as their key).
		game_rules: GameRules object.

	Returns:
		A dict from Deck to list of DevelopmentCards.
	"""
	revealed_cards = collections.defaultdict(list)
	cards_per_level = game_rules.num_cards_revealed_per_level
	for deck, cards in development_cards_dict.iteritems():
		revealed_cards[deck] = cards[-cards_per_level:]
	return revealed_cards


def CountPoints(player_state):
	"""Returns the number of points given a PlayerState."""
	num_points = 0
	for card in player_state.purchased_cards:
		num_points += card.points
	for noble_tile in player_state.noble_tiles:
		num_points += noble_tile.points
	return num_points

def GetCardByID(player_game_state, card_id):
        for deck in xrange(1, 4):
                for card in player_game_state.revealed_cards[deck]:
                        if card.asset_id == card_id:
                                 return card
        for card in self_state.reserved_cards:
                if card.asset_id == card_id:
                        return card
        return False

def GetNobleById(player_game_state, noble_id):
        for noble in player_game_state.noble_tiles:
            if noble.asset_id == noble_id:
                return noble
        return False

class SelfState(object):
	"""Wrapper for PlayerState."""
	def __init__(self, player_state):
		"""Precomputes relevant values of player_state."""
		self._player_state = player_state
		self._gem_counts = gem_utils.CountGems(player_state.gems)
		self._unhidden_reserved_cards = player_state.unhidden_reserved_cards
		self._hidden_reserved_cards = player_state.hidden_reserved_cards
		
		# Derived values from a player's purchased cards and nobles.
		self._num_points = CountPoints(player_state)
		self._gem_discounts = collections.defaultdict(int)  # keyed by GemType
		for card in player_state.purchased_cards:
			self._gem_discounts[card.gem.type] += 1

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


class OpponentState(SelfState):
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
		self._revealed_cards = GetRevealedCards(
			game_state.development_cards, game_rules)
                self._noble_tiles = game_state.noble_tiles
		# The order of 'self._opponent_states' respects the turn
		# ordering, starting with the next player's state.
		self._opponent_states = []
		num_players = len(game_state.player_states)
		num_opponents = num_players - 1
		for i in range(num_opponents):
			opponent_idx = (i + game_state.turn + 1) % num_players
			self._opponent_states.append(OpponentState(
				game_state.player_states[opponent_idx]))
		curr_player_idx = game_state.turn
		self._self_state = SelfState(
			game_state.player_states[curr_player_idx])

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
    
        def GemLimit(self):
                return self._game_rules.max_gems - sum(self._self_state.gem_counts)

        def CanReserve(self):
                return self._self_state.num_reserved_cards < self._game_rules.max_reserved_cards


	@property
	def gem_counts(self):
		return self._gem_counts

	@property
	def revealed_cards(self):
		return self._revealed_cards

        @property
        def noble_tiles(self):
                return self._noble_tiles

	@property
	def self_state(self):
		return self._self_state
	
	@property
	def opponent_states(self):
		return self._opponent_states
	
