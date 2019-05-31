from src.proto.development_card_proto import DevelopmentCard
from src.proto.development_card_proto import GemType

# TODO: fill in with actual first level card values
FIRST_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="100",
		level=1,
		points=1,
		gem=GemType.BLUE,
		blue_cost=0,
		green_cost=0,
		red_cost=4,
		white_cost=0,
		brown_cost=0
	),
]
