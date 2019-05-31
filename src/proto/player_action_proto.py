"""Data schema for a player's action."""

import collections

PlayerAction = collections.namedtuple(
  "PlayerAction", [
    # Number of gold gems taken.
    "gold_taken",

    # Number of blue gems taken.
    "blue_taken",

    # Number of green gems taken.
    "green_taken",

    # Number of red gems taken.
    "red_taken",

    # Number of brown gems taken.
    "brown_taken",

    # Number of white gems taken.
    "white_taken",

    # Number of gold gems returned.
    "gold_returned",

    # Number of blue gems returned.
    "blue_returned",

    # Number of green gems returned.
    "green_returned",

    # Number of red gems returned.
    "red_returned",

    # Number of brown gems returned.
    "brown_returned",

    # Number of white gems returned.
    "white_returned",

    # Purchased DevelopmentCard::asset_id.
    "purchased_card_id",

    # Reserved DevelopmentCard::asset_id.
    "reserved_card_id",

    # Which deck to reserve from if topdecking.
    "topdeck_level",
  ])
