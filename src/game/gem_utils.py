"""Utils for handling and organizing Gems."""

import collections


def CountGems(gems_list):
	"""Returns dict of (GemType, count) of list of GemTypes."""
	counts = collections.defaultdict(int)
	for gem in gems_list:
		counts[gem] += 1
	return counts


def GetGems(gem_counts):
	"""Returns a list of GemTypes given a dict from GemType to counts."""
	gems_list = []
	for gem_type, count in gem_counts.iteritems():
		if count < 0:
			raise NotImplementedError("count cannot be negative")
		for _ in range(count):
			gems_list.append(gem_type)
	return gems_list


def GetDiscountedCost(cost, discount):
	"""Returns the subtraction between cost and discount dicts"""
	return collections.Counter(cost) - collections.Counter(discount)

