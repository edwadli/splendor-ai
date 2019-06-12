"""Data schema for the history of a game."""

import collections

GameHistory = collections.namedtuple(
  "GameHistory", [
    # The game rules used to initialize the game.
    "game_rules",

    # The starting state of the game.
    "initial_game_state",

    # The list of PlayerActions that have been taken so far. Note that
    # given an index, i, from this list,
    # i%len(initial_game_state.player_states) corresponds to the player_states
    # index.
    "player_action_history",
  ])
