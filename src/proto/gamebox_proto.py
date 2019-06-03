"""Data schema for Gamebox."""

import collections

Gamebox = collections.namedtuple(
  "Gamebox", [
    # Gems available. A defaultdict(int) keyed by GemType.
    "gems",

    # Development cards available.
    "development_cards",

    # NobleTiles available.
    "noble_tiles",

    # The GameRules.
    "game_rules",
  ])
