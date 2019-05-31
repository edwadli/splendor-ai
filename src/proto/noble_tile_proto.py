"""Data schema for a Noble Tile."""

import collections

NobleTile = collections.namedtuple(
  "NobleTile", [
    # Number of points the tile is worth.
    "points",

    # Number of blue development cards this tile requires.
    "blue_card_cost",

    # Number of green development cards this tile requires.
    "green_card_cost",

    # Number of red development cards this tile requires.
    "red_card_cost",

    # Number of white development cards this tile requires.
    "white_card_cost",

    # Number of brown development cards this tile requires.
    "brown_card_cost",
  ])
