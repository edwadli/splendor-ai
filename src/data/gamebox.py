from src.data import first_level_cards
from src.data import game_rules
from src.data import noble_tiles
from src.data import second_level_cards
from src.data import third_level_cards
from src.proto.gamebox_proto import Gamebox

GAMEBOX = Gamebox(
	num_gold_gems=5,
	num_blue_gems=7,
	num_green_gems=7,
	num_red_gems=7,
	num_brown_gems=7,
	num_white_gems=7,
	first_level_cards=first_level_cards.FIRST_LEVEL_CARDS,
	second_level_cards=second_level_cards.SECOND_LEVEL_CARDS,
	third_level_cards=third_level_cards.THIRD_LEVEL_CARDS,
	noble_tiles=noble_tiles.NOBLE_TILES,
	game_rules=game_rules.GAME_RULES
)
