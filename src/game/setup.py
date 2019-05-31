"""Utils for setting up the game."""

from src.proto.game_state_proto import GameState
from src.proto.player_state_proto import PlayerState

def NewPlayerState():
	"""Returns a new player's state."""
	player_state = PlayerState(
		num_gold_gems=0,
		num_blue_gems=0,
		num_green_gems=0,
		num_red_gems=0,
		num_brown_gems=0,
		num_white_gems=0,
		purchased_cards=[],
		reserved_cards=[],
		hidden_reserved_cards=[],
		noble_tiles=[],
	)
	return player_state


def InitializeGameState(gamebox, num_players):
	"""Returns a new game's state given a Gamebox and number of players."""
	game_state = GameState(
		num_gold_gems=gamebox.num_gold_gems,
		num_blue_gems=gamebox.num_blue_gems,
		num_green_gems=gamebox.num_green_gems,
		num_red_gems=gamebox.num_red_gems,
		num_brown_gems=gamebox.num_brown_gems,
		num_white_gems=gamebox.num_white_gems,
		first_level_cards=gamebox.first_level_cards,
		second_level_cards=gamebox.second_level_cards,
		third_level_cards=gamebox.third_level_cards,
		noble_tiles=gamebox.noble_tiles,
		player_states=[NewPlayerState() for _ in range(num_players)],
		turn=0,
	)
	return game_state
