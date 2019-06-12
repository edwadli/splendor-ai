"""Data schema for the result of a game."""

import collections

GameResult = collections.namedtuple(
  "GameResult", [
    # A list of agent ids. Must correspond to the PlayerStates in
    # 'final_game_state.player_states'.
    "agent_ids",

    # The list of winners (indices into 'agent_ids').
    "winners",

    # The GameState at the end of the game.
    "final_game_state",

    # The number of rounds played.
    "num_rounds_played",

    # The GameHistory.
    "game_history",
  ])
