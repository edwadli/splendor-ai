from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard
from src.proto.gem_proto import GemType

# TODO: fill in with actual first level card values
FIRST_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="100",
		level=Deck.LEVEL_1,
		points=1,
		gem=GemType.BLUE,
		cost={GemType.RED: 4},
	),
]
