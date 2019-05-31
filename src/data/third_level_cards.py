from src.proto.development_card_proto import DevelopmentCard
from src.proto.development_card_proto import GemType

# TODO: fill in with actual third level card values
THIRD_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="300",
		level=3,
		points=4,
		gem=GemType.BLUE,
		blue_cost=0,
		green_cost=0,
		red_cost=0,
		white_cost=7,
		brown_cost=0
	),
]
