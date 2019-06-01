"""Data schema for a Development Card."""

import collections

DevelopmentCard = collections.namedtuple(
  "DevelopmentCard", [
    # The game piece's globally unique asset id.
    "asset_id",

    # The card's level (of type Deck).
    "level",

    # Number of points the card is worth.
    "points",

    # The Gem discount the card offers.
    "gem",

    # The list of gems this card costs.
    "cost",
  ])
