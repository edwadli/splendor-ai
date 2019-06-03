from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard
from src.proto.gem_proto import GemType

# TODO: fill in with actual third level card values
THIRD_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="300",
		level=Deck.LEVEL_3,
		points=4,
		gem=GemType.BLUE,
		cost={GemType.WHITE: 7},
	),
]
