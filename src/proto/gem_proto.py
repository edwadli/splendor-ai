"""Data schema for a gem."""

import collections

Gem = collections.namedtuple(
	"Gem", [
		# The GemType (color).
		"type",
	])

class GemType:
  BLUE = 1
  GREEN = 2
  RED = 3
  WHITE = 4
  BROWN = 5
  GOLD = 6
