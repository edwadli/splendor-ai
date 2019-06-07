import collections

from src.proto.noble_tile_proto import NobleTile
from src.proto.gem_proto import GemType

NOBLE_TILES = [
	NobleTile(
		asset_id="900",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.BROWN: 4,
			GemType.RED: 4}),
	),
	NobleTile(
		asset_id="901",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.RED: 4,
			GemType.GREEN: 4}),
	),
	NobleTile(
		asset_id="902",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.GREEN: 4,
			GemType.BLUE: 4}),
	),
	NobleTile(
		asset_id="903",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.BLUE: 4,
			GemType.WHITE: 4}),
	),
	NobleTile(
		asset_id="904",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.WHITE: 4,
			GemType.BROWN: 4}),
	),
	NobleTile(
		asset_id="905",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.WHITE: 3,
			GemType.BLUE: 3,
			GemType.BROWN: 3}),
	),
	NobleTile(
		asset_id="906",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.BLUE: 3,
			GemType.RED: 3,
			GemType.GREEN: 3}),
	),
	NobleTile(
		asset_id="907",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.BROWN: 3,
			GemType.RED: 3,
			GemType.WHITE: 3}),
	),
	NobleTile(
		asset_id="908",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.BLUE: 3,
			GemType.GREEN: 3,
			GemType.WHITE: 3}),
	),
	NobleTile(
		asset_id="909",
		points=3,
		gem_type_requirements=collections.defaultdict(int, {
			GemType.BROWN: 3,
			GemType.GREEN: 3,
			GemType.RED: 3}),
	),
]
