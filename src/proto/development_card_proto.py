"""Data schema for a Development Card."""

import collections

DevelopmentCard = collections.namedtuple(
  "DevelopmentCard", [
    # The card's globally unique asset id.
    "asset_id",

    # The card's level.
    "level",

    # Number of points the card is worth.
    "points",

    # The GemType discount the card offers.
    "gem",

    # Number of blue gems this card costs.
    "blue_cost",

    # Number of green gems this card costs.
    "green_cost",

    # Number of red gems this card costs.
    "red_cost",

    # Number of white gems this card costs.
    "white_cost",

    # Number of brown gems this card costs.
    "brown_cost",
  ])

class GemType:
  BLUE = 1
  GREEN = 2
  RED = 3
  WHITE = 4
  BROWN = 5
