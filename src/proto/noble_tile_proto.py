"""Data schema for a Noble Tile."""

import collections

NobleTile = collections.namedtuple(
  "NobleTile", [
    # The game piece's globally unique asset id.
    "asset_id",

    # Number of points the tile is worth.
    "points",

    # The list of GemType discounts that this tile requires.
    "gem_type_requirements",
  ])
