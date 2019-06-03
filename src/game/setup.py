"""Utils for setting up the game."""

import collections
import copy
import random

from src.game import gem_utils
from src.proto.deck_proto import Deck
from src.proto.game_state_proto import GameState
from src.proto.gem_proto import GemType
from src.proto.development_card_proto import DevelopmentCard
from src.proto.noble_tile_proto import NobleTile
from src.proto.player_state_proto import PlayerState

def NewPlayerState():
	"""Returns a new player's state."""
	player_state = PlayerState(
		gems = {GemType.BLUE: 0, GemType.GREEN: 0, GemType.RED: 0, GemType.WHITE: 0, GemType.BROWN: 0, GemType.GOLD: 0},
		purchased_cards=[],
		unhidden_reserved_cards=[],
		hidden_reserved_cards=[],
		noble_tiles=[],
	)
	return player_state


def InitializeGameState(gamebox, num_players, random_seed=None):
	"""Returns a new game's state given a Gamebox and number of players."""
	game_rules = gamebox.game_rules
	if (num_players < game_rules.min_players or
		num_players > game_rules.max_players):
		raise NotImplementedError("This game does not support " +
			str(num_players) + " players")

	# Reduce non-gold gem counts, if necessary.
	gem_counts = copy.deepcopy(gamebox.gems)
	gem_reduction_amount = (
		game_rules.nongold_gem_removals_by_num_players[num_players])
        for gem_type in gem_counts.keys():
		if gem_type == GemType.GOLD:
			continue  # only reduce non-gold gems
		gem_counts[gem_type] -= gem_reduction_amount
	randomizer = random.Random(random_seed)

	# Separate the cards by level.
	development_cards = collections.defaultdict(list)
	for card in gamebox.development_cards:
		development_cards[card.level].append(card)
	# Shuffle all the cards.
	for cards in development_cards.values():
		randomizer.shuffle(cards)

	# Shuffle and deal the noble tiles.
	noble_tiles = randomizer.sample(
		gamebox.noble_tiles, num_players + 1)

	game_state = GameState(
		available_gems=gem_counts,
		development_cards=development_cards,
		noble_tiles=noble_tiles,
		player_states=[NewPlayerState() for _ in range(num_players)],
		turn=0,
	)
	return game_state


def EmptyBlueDevelopmentCard():
	"""Returns an empty, blue, level 1, free development card."""
	card = DevelopmentCard(
		asset_id="",
		level=Deck.LEVEL_1,
		points=0,
		gem=GemType.BLUE,
		cost={}
	)
	return card


def EmptyNobleTile():
	"""Returns a free, 0-point noble tiles."""
	noble_tile = NobleTile(
		asset_id="",
		points=0,
		gem_type_requirements={}
	)
	return noble_tile


def SinglePlayerEmptyGameState():
	"""Returns an empty game state with a single player."""
	game_state = GameState(
		available_gems= {GemType.BLUE: 0, GemType.GREEN: 0, GemType.RED: 0, GemType.WHITE: 0, GemType.BROWN: 0, GemType.GOLD: 0},
		development_cards=collections.defaultdict(list),
		noble_tiles=[],
		player_states = [NewPlayerState()],
		turn = 0
	)
	return game_state
