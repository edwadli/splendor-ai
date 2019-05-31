"""Data schema for Gamebox."""

import collections

Gamebox = collections.namedtuple(
  "Gamebox", [
    # Number of gold gems.
    "num_gold_gems",

    # Number of blue gems.
    "num_blue_gems",

    # Number of green gems.
    "num_green_gems",

    # Number of red gems.
    "num_red_gems",

    # Number of brown gems.
    "num_brown_gems",

    # Number of white gems.
    "num_white_gems",        

    # The level 1 DevelopmentCards.
    "first_level_cards",

    # The level 2 DevelopmentCards.
    "second_level_cards",

    # The level 3 DevelopmentCards.
    "third_level_cards",

    # NobleTiles available.
    "noble_tiles",

    # The GameRules.
    "game_rules",
  ])
