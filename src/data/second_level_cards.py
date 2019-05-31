from src.proto.development_card_proto import DevelopmentCard
from src.proto.development_card_proto import GemType

# TODO: fill in with actual second level card values
SECOND_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="200",
		level=2,
		points=3,
		gem=GemType.BLUE,
		blue_cost=6,
		green_cost=0,
		red_cost=0,
		white_cost=0,
		brown_cost=0
	),
]
