from src.data import gems
from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard

# TODO: fill in with actual first level card values
FIRST_LEVEL_CARDS = [
	DevelopmentCard(
		asset_id="100",
		level=Deck.LEVEL_1,
		points=1,
		gem=gems.BLUE,
		cost=([gems.RED] * 4),
	),
]
