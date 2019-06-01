from src.data import gems
from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard

# TODO: fill in with actual second level card values
SECOND_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="200",
		level=Deck.LEVEL_2,
		points=3,
		gem=gems.BLUE,
		cost=([gems.BLUE] * 6),
	),
]
