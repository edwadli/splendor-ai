"""Tests for engine.py"""

import unittest

from src.data import gamebox
from src.data import player_action
from src.game import engine
from src.game import setup
from src.game.player_game_state import PlayerGameState
from src.proto.deck_proto import Deck
from src.proto.game_state_proto import GameState
from src.proto.gem_proto import GemType

class TestEngine(unittest.TestCase):

    def test_CheckPlayerAction(self):
        num_players = 4
        game_state = setup.InitializeGameState(gamebox.GAMEBOX, num_players, random_seed=0)
        game_rules = gamebox.GAMEBOX.game_rules
        player_game_state = PlayerGameState(game_state, game_rules)
        result = engine.check_player_action(player_game_state, player_action.PLAYER_ACTION)
        self.assertIsNone(result)


