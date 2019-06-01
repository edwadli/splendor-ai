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
			[GemType.BROWN] * 4),
	),
]
