"""Data schema for Game Rules.

Includes magic constants from game rules.
"""

import collections

GameRules = collections.namedtuple(
  "NobleTile", [
    # Number of points to win the game.
    "points_to_win",

    # Max number of gems that can be held by a player.
    "max_gems",

    # Max number of reserved DevelopmentCards a player can have.
    "max_reserved_cards",

    # Minimum number of gems available so that player can take two.
    "min_double_take_gems",

    # Number of cards revealed per level.
    "num_cards_revealed_per_level",
  ])
