"""Data schema for a player's state."""

import collections

PlayerState = collections.namedtuple(
  "PlayerState", [
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

    # Purchased DevelopmentCards.
    "purchased_cards",

    # Reserved DevelopmentCards.
    "reserved_cards",

    # Hidden (reserved) DevelopmentCards. Note that reserved cards are
    # typically hidden when topdecked.
    "hidden_reserved_cards",

    # NobleTiles obtained.
    "noble_tiles",
  ])
