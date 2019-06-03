from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard
from src.proto.gem_proto import GemType

# TODO: fill in with actual second level card values
SECOND_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="200",
		level=Deck.LEVEL_2,
		points=3,
		gem=GemType.BLUE,
		cost={GemType.BLUE: 6},
	),
]
