"""Utils for handling and organizing Gems."""

import collections

from src.proto.gem_proto import Gem


def CountGems(gems_list):
	"""Returns dict of (GemType, count) of list of gems."""
	counts = collections.defaultdict(int)
	for gem in gems_list:
		counts[gem.type] += 1
	return counts

def GetGems(gem_counts):
	"""Returns a list of Gems given a dict from GemType to counts."""
	gems_list = []
	for gem_type, count in gem_counts:
		gems_list.append(Gem(type=gem_type))
	return gems_list
