"""Data schema for a player's action."""

import collections

PlayerAction = collections.namedtuple(
  "PlayerAction", [
    # List of Gems taken from the field.
    "gems_taken",

    # List of Gems returned to the field.
    "gems_returned",

    # Purchased DevelopmentCard::asset_id.
    "purchased_card_id",

    # Reserved DevelopmentCard::asset_id.
    "reserved_card_id",

    # Which Deck to reserve from if topdecking.
    "topdeck_level",

    # Claimed NobleTile::asset_id.
    "noble_tile_id",
  ])
