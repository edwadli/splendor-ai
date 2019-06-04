"""Utils for handling and organizing Gems."""

import collections

from src.proto.gem_proto import GemType


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


def GemDifference(gems_a, gems_b):
	"""Returns the subtraction between 'gems_a' and discount 'gems_b'"""
	return collections.Counter(gems_a) - collections.Counter(gems_b)


def GetDiscountedCost(cost, discount):
	"""Returns the gems cost after discount."""
	if cost[GemType.GOLD] != 0 or discount[GemType.GOLD] != 0:
		raise ValueError("Cost and discount cannot include GOLD GemType")
	discounted_cost = GemDifference(cost, discount)
	for gem_type in discounted_cost:
		discounted_cost[gem_type] = max(discounted_cost[gem_type], 0)
	return discounted_cost


def CanTakeFrom(gems_available, gems_taken):
	"""Returns whether 'gems_taken' can be taken from 'gems_available'."""
	return all(
	    diff >= 0 for diff in GemDifference(gems_available, gems_taken))


def ExactlyPaysFor(cost, payment):
	"""Returns whether the 'cost' is exactly covered by 'payment'."""
	if cost[GemType.GOLD] != 0:
		raise ValueError("Cost cannot include GOLD GemType")
	gold_needed = 0
	for gem_type in cost:
		if gem_type == GemType.GOLD:
			continue
		gem_diff = cost[gem_type] - payment[gem_type]
		if gem_diff > 0:
			gold_needed += gem_diff
		elif gem_diff < 0:
			return False  # too many gems of this type were paid
	return gold_needed == payment[GemType.GOLD]


def NumGems(gems):
	"""Returns the number of gems in the defaultdict(int)."""
	return sum(gems.values())


def NumNonGoldGems(gems):
	"""Returns the number of non-gold gems in the defaultdict(int)."""
	return sum(count for gem_type, count in gems.iteritems()
	           if gem_type != GemType.GOLD)


def VerifyNonNegativeGems(gems):
	"""Returns that all gem values are nonnegative."""
	return all(count >= 0 for count in gems.values())


def AllZerosExcept(gems, *gem_types):
	for gem_type, count in gems.iteritems():
		if gem_type in gem_types:
			continue
		if count != 0:
			return False
	return True


def GetNonEmptyGemTypes(gems):
	non_empty_types = []
	for gem_type, count in gems.iteritems():
		if count <= 0:
			continue
		non_empty_types.append(gem_type)
	return non_empty_types
