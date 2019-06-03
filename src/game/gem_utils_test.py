"""Tests for gem_utils.py"""

import unittest

from src.game import gem_utils
from src.proto.gem_proto import GemType


class TestGemUtils(unittest.TestCase):

	def test_CountGems(self):
		gems_list = [GemType.RED, GemType.BLUE, GemType.RED]
		gem_counts = gem_utils.CountGems(gems_list)
		self.assertEquals(gem_counts, {
			GemType.RED: 2,
			GemType.BLUE: 1,
		})

	def test_CountGemsEmpty(self):
		gem_counts = gem_utils.CountGems([])
		self.assertEquals(len(gem_counts), 0)

	def test_GetGems(self):
		gem_counts = {
			GemType.GOLD: 3,
			GemType.BROWN: 1,
			GemType.WHITE: 0,
		}
		gems_list = gem_utils.GetGems(gem_counts)
		self.assertEquals(sorted(gems_list), [
			GemType.BROWN,
			GemType.GOLD,
			GemType.GOLD,
			GemType.GOLD,
		])


if __name__ == "__main__":
	unittest.main()
