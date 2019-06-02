"""Tests for driver.py"""

import collections
import unittest

from src.data import game_rules
from src.data import gamebox
from src.game import agent
from src.game import driver
from src.game import setup
from src.proto.development_card_proto import DevelopmentCard
from src.proto.game_state_proto import GameState
from src.proto.noble_tile_proto import NobleTile
from src.proto.player_state_proto import PlayerState


class FakeAgent(agent.Agent):
  def PlayTurn(self, player_game_state):
    pass  # TODO


class TestDriver(unittest.TestCase):

  def _GetWinningPlayerState(self):
    """Helper method that returns a winning player state."""
    player_state = setup.NewPlayerState()._replace(
      purchased_cards=[
        setup.EmptyBlueDevelopmentCard()._replace(points=5),
        setup.EmptyBlueDevelopmentCard()._replace(points=4),
      ],
      noble_tiles=[
        setup.EmptyNobleTile()._replace(points=3),
        setup.EmptyNobleTile()._replace(points=3),
      ])
    return player_state

  def test_DriverInitializesWithGamebox(self):
    agents = [FakeAgent(), FakeAgent()]
    self.assertIsNotNone(
      driver.Driver(agents, gamebox=gamebox.GAMEBOX))

  def test_DriverInitializesWithGameboxAndSeed(self):
    agents = [FakeAgent(), FakeAgent()]
    self.assertIsNotNone(
      driver.Driver(agents, gamebox=gamebox.GAMEBOX,
              random_seed=0))

  def test_DriverInitializesWithGameState(self):
    agents = [FakeAgent(), FakeAgent()]
    game_state = setup.SinglePlayerEmptyGameState()._replace(
      player_states=[
        setup.NewPlayerState(), setup.NewPlayerState()])
    self.assertIsNotNone(driver.Driver(
      agents, game_state=game_state, game_rules=game_rules.GAME_RULES))

  def test_DriverInitializesWithGameStateWrongNumAgentsFails(self):
    agents = [FakeAgent(), FakeAgent(), FakeAgent()]
    game_state = setup.SinglePlayerEmptyGameState()._replace(
      player_states=[
        setup.NewPlayerState(), setup.NewPlayerState()])
    with self.assertRaises(IndexError):
      driver.Driver(
        agents, game_state=game_state,
        game_rules=game_rules.GAME_RULES)

  def test_DriverInitializesWithWrongAgentTypeFails(self):
    agents = [None, None]
    with self.assertRaises(TypeError):
      driver.Driver(agents, gamebox=gamebox.GAMEBOX)

  def test_DriverGetWinner(self):
    agents = [FakeAgent(), FakeAgent()]
    game_state = setup.SinglePlayerEmptyGameState()._replace(
      player_states=[
        setup.NewPlayerState(),
        self._GetWinningPlayerState(),
      ],
      turn=0,
    )
    game_driver = driver.Driver(
      agents, game_state=game_state,
      game_rules=game_rules.GAME_RULES)
    winners = game_driver.GetWinner()
    self.assertEquals(winners, (1,))

  def test_DriverWinnerButNeedToCompleteRound(self):
    agents = [FakeAgent(), FakeAgent()]
    game_state = setup.SinglePlayerEmptyGameState()._replace(
      player_states=[
        setup.NewPlayerState(),
        self._GetWinningPlayerState(),
      ],
      turn=1,
    )
    game_driver = driver.Driver(
      agents, game_state=game_state,
      game_rules=game_rules.GAME_RULES)
    winners = game_driver.GetWinner()
    self.assertEquals(winners, tuple())

  def test_DriverGetWinnerWithTieBreak(self):
    agents = [FakeAgent(), FakeAgent()]
    game_state = setup.SinglePlayerEmptyGameState()._replace(
      player_states=[
        self._GetWinningPlayerState(),
        setup.NewPlayerState()._replace(
          purchased_cards=[
            setup.EmptyBlueDevelopmentCard()._replace(points=15),
          ]),
      ],
      turn=0,
    )
    game_driver = driver.Driver(
      agents, game_state=game_state,
      game_rules=game_rules.GAME_RULES)
    winners = game_driver.GetWinner()
    self.assertEquals(winners, (1,))

  def test_DriverGetWinnerTie(self):
    agents = [FakeAgent(), FakeAgent()]
    game_state = setup.SinglePlayerEmptyGameState()._replace(
      player_states=[
        self._GetWinningPlayerState(),
        self._GetWinningPlayerState(),
      ],
      turn=0,
    )
    game_driver = driver.Driver(
      agents, game_state=game_state,
      game_rules=game_rules.GAME_RULES)
    winners = game_driver.GetWinner()
    self.assertEquals(winners, (0, 1))

  def test_DriverGetWinnerNone(self):
    agents = [FakeAgent(), FakeAgent()]
    game_state = setup.SinglePlayerEmptyGameState()._replace(
      player_states=[
        setup.NewPlayerState(),
        setup.NewPlayerState(),
      ],
      turn=0,
    )
    game_driver = driver.Driver(
      agents, game_state=game_state,
      game_rules=game_rules.GAME_RULES)
    winners = game_driver.GetWinner()
    self.assertEquals(winners, tuple())

  def test_DriverRunAgentTurn(self):
    # TODO
    self.assertTrue(True)


if __name__ == "__main__":
  unittest.main()
