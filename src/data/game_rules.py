from src.proto.game_rules_proto import GameRules

GAME_RULES = GameRules(
	points_to_win=15,
	max_gems=10,
	max_reserved_cards=3,
	min_double_take_gems=4,
	num_cards_revealed_per_level=4,
)
