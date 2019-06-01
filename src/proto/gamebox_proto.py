"""Data schema for Gamebox."""

import collections

Gamebox = collections.namedtuple(
  "Gamebox", [
    # Gems available.
    "gems",

    # Development cards available.
    "development_cards",

    # NobleTiles available.
    "noble_tiles",

    # The GameRules.
    "game_rules",
  ])
