"""Data schema for a game state."""

import collections

GameState = collections.namedtuple(
  "GameState", [
    # The Gems available for taking.
    "available_gems",

    # The DevelopmentCards on the field. This is a defaultdict(list)
    # from Deck to list of DevelopmentCards. The last N cards in each list
    # are revealed and available for taking.
    "development_cards",

    # NobleTiles available.
    "noble_tiles",

    # The list of PlayerStates. The order corresponds to the order of
    # play.
    "player_states",

    # The index (to 'player_states') indicating whose turn it is.
    "turn",
  ])

class Deck:
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
