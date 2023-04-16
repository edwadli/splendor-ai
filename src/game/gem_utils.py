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
	for gem_type, count in gem_counts.items():
		if count < 0:
			raise NotImplementedError("count cannot be negative")
		for _ in range(count):
			gems_list.append(gem_type)
	return gems_list


def GetDiscountedCost(cost, discount):
	"""Returns the gems cost after discount."""
	if cost[GemType.GOLD] != 0:
		raise ValueError("Cost cannot include GOLD GemType")
	discounted_cost = collections.Counter(cost) - collections.Counter(discount)
	return discounted_cost


def CanTakeFrom(gems_available, gems_taken):
	"""Returns whether 'gems_taken' can be taken from 'gems_available'."""
	for gem_type, count in gems_taken.items():
		if gems_available[gem_type] < count:
			return False
	return True


def CanPayFor(cost, payment, is_exact=False):
	"""Returns whether the 'cost' is exactly covered by 'payment'."""
	if cost[GemType.GOLD] != 0:
		raise ValueError("Cost cannot include GOLD GemType")
	gold_needed = 0
	for gem_type in cost:
		gem_diff = cost[gem_type] - payment[gem_type]
		if gem_diff > 0:
			gold_needed += gem_diff
		elif gem_diff < 0 and is_exact:
			return False  # too many gems of this type were paid
	if is_exact:
		return gold_needed == payment[GemType.GOLD]
	else:
		return gold_needed <= payment[GemType.GOLD]


def ExactlyPaysFor(cost, payment):
	return CanPayFor(cost, payment, is_exact=True)


def NumGems(gems):
	"""Returns the number of gems in the defaultdict(int)."""
	return sum(gems.values())


def NumNonGoldGems(gems):
	"""Returns the number of non-gold gems in the defaultdict(int)."""
	return sum(count for gem_type, count in gems.items()
	           if gem_type != GemType.GOLD)


def GetMaxCountGems(gems):
	"""Returns the list of GemTypes that have the highest count."""
	max_count = max(gems.values())
	max_gems = [gem for gem, count in gems.items()
							if count == max_count]
	return max_gems


def GemsByCount(gems, reverse=False):
	"""Returns a list of GemTypes from lowest to highest count."""
	gem_types = list(gems.keys())
	gem_types.sort(key=lambda k: gems[k], reverse=reverse)
	return gem_types


def VerifyNonNegativeGems(gems):
	"""Returns that all gem values are nonnegative."""
	return all(count >= 0 for count in gems.values())


def AllZerosExcept(gems, *gem_types):
	for gem_type, count in gems.items():
		if gem_type in gem_types:
			continue
		if count != 0:
			return False
	return True


def GetNonEmptyGemTypes(gems):
	non_empty_types = []
	for gem_type, count in gems.items():
		if count <= 0:
			continue
		non_empty_types.append(gem_type)
	return non_empty_types
