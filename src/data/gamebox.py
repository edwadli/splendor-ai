from src.data import first_level_cards
from src.data import game_rules
from src.data import gems
from src.data import noble_tiles
from src.data import second_level_cards
from src.data import third_level_cards
from src.proto.gamebox_proto import Gamebox

GAMEBOX = Gamebox(
	gems=(
		[gems.GOLD] * 5 +
		[gems.BLUE] * 7 +
		[gems.GREEN] * 7 +
		[gems.RED] * 7 +
		[gems.BROWN] * 7 +
		[gems.WHITE] * 7),
	development_cards=(
		first_level_cards.FIRST_LEVEL_CARDS +
		second_level_cards.SECOND_LEVEL_CARDS +
		third_level_cards.THIRD_LEVEL_CARDS),
	noble_tiles=noble_tiles.NOBLE_TILES,
	game_rules=game_rules.GAME_RULES
)
