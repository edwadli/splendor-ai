"""Data schema for a player's state."""

import collections

PlayerState = collections.namedtuple(
  "PlayerState", [
    # List of Gems held by player.
    "gems",

    # List of purchased DevelopmentCards.
    "purchased_cards",

    # List of reserved (non-hidden) DevelopmentCards.
    "unhidden_reserved_cards",

    # List of reserved (hidden) DevelopmentCards. Note that reserved cards are
    # typically hidden when topdecked.
    "hidden_reserved_cards",

    # NobleTiles obtained.
    "noble_tiles",
  ])
