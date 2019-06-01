from src.proto.noble_tile_proto import NobleTile
from src.proto.gem_proto import GemType

# TODO: fill in with actual tile values
NOBLE_TILES = [
	NobleTile(
		asset_id="900",
		points=3,
		gem_type_requirements=(
			[GemType.BLUE] * 4 +
			[GemType.GREEN] * 4),
	),
	NobleTile(
		asset_id="901",
		points=3,
		gem_type_requirements=(
			[GemType.RED] * 4 +
			[GemType.WHITE] * 4),
	),
	NobleTile(
		asset_id="902",
		points=3,
		gem_type_requirements=(
			[GemType.GREEN] * 4 +
			[GemType.BROWN] * 4),
	),
	NobleTile(
		asset_id="903",
		points=3,
		gem_type_requirements=(
			[GemType.BLUE] * 3 +
			[GemType.RED] * 3 +
			[GemType.WHITE] * 3),
	),
	NobleTile(
		asset_id="904",
		points=3,
		gem_type_requirements=(
			[GemType.BROWN] * 3 +
			[GemType.BLUE] * 3 +
			[GemType.WHITE] * 3),
	),
	NobleTile(
		asset_id="905",
		points=3,
		gem_type_requirements=(
			[GemType.BLUE] * 3 +
			[GemType.GREEN] * 3 +
			[GemType.WHITE] * 3),
	),
]
