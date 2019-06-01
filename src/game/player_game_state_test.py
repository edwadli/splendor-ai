"""Tests for player_game_state.py"""

import unittest

# TODO: use test data instead of real game_rules itself.
from src.data import game_rules
from src.data import gems
from src.game import gem_utils
from src.game import player
from src.game import player_game_state
from src.game import setup
from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard
from src.proto.gem_proto import GemType
from src.proto.player_state_proto import PlayerState


class TestPlayerGameState(unittest.TestCase):

	def test_GetRevealedCards(self):
		dev_card_1 = DevelopmentCard(
			asset_id="",
			level=Deck.LEVEL_1,
			points=0,
			gem=gems.RED,
			cost=[gems.RED, gems.BLUE, gems.WHITE, gems.GREEN])
		dev_card_2 = DevelopmentCard(
			asset_id="",
			level=Deck.LEVEL_2,
			points=3,
			gem=gems.RED,
			cost=[gems.RED] * 6)
		development_cards = {
			Deck.LEVEL_1: [dev_card_1] * 5,
			Deck.LEVEL_2: [dev_card_2],
			Deck.LEVEL_3: [],
		}
		result_cards = player_game_state.GetRevealedCards(
			development_cards, game_rules.GAME_RULES)
		self.assertEquals(result_cards, {
			Deck.LEVEL_1: [dev_card_1] * 4,
			Deck.LEVEL_2: [dev_card_2],
			Deck.LEVEL_3: [],
		})

	def test_OpponentStateIsPlayer(self):
		opponent_state = player_game_state.OpponentState(
			setup.NewPlayerState())
		self.assertIsInstance(opponent_state, player.Player)
		with self.assertRaises(AttributeError):
			_ = opponent_state.PlayTurn(None)

	def test_OpponentStateHidesHiddenReservedCards(self):
		player_state = setup.NewPlayerState()
		player_state.hidden_reserved_cards.append(DevelopmentCard(
			asset_id="",
			level=Deck.LEVEL_1,
			points=0,
			gem=gems.RED,
			cost=[]))
		opponent_state = player_game_state.OpponentState(player_state)
		with self.assertRaises(AttributeError):
			_ = opponent_state.player_state
		with self.assertRaises(AttributeError):
			_ = opponent_state.hidden_reserved_cards
		self.assertEquals(opponent_state.num_hidden_reserved_cards, 1)

	def test_PlayerGameStateCanTakeTwo(self):
		game_state = setup.SinglePlayerEmptyGameState()._replace(
			available_gems=[gems.RED] * 4)
		state = player_game_state.PlayerGameState(
			game_state, game_rules.GAME_RULES)
		self.assertTrue(state.CanTakeTwo(GemType.RED))

	def test_PlayerGameStateCannotTakeTwo(self):
		game_state = setup.SinglePlayerEmptyGameState()._replace(
			available_gems=[gems.RED] * 3)
		state = player_game_state.PlayerGameState(
			game_state, game_rules.GAME_RULES)
		self.assertFalse(state.CanTakeTwo(GemType.RED))

	def test_PlayerGameStateCanTopDeck(self):
		game_state = setup.SinglePlayerEmptyGameState()._replace(
			development_cards={
				Deck.LEVEL_1: [setup.EmptyBlueDevelopmentCard()] * 5,
				Deck.LEVEL_2: [setup.EmptyBlueDevelopmentCard()] * 4,
			})
		state = player_game_state.PlayerGameState(
			game_state, game_rules.GAME_RULES)
		self.assertEquals(state.revealed_cards, {
				Deck.LEVEL_1: [setup.EmptyBlueDevelopmentCard()] * 4,
				Deck.LEVEL_2: [setup.EmptyBlueDevelopmentCard()] * 4,
			})
		self.assertTrue(state.CanTopDeck(Deck.LEVEL_1))
		self.assertFalse(state.CanTopDeck(Deck.LEVEL_2))

	def test_PlayerGameStateHasOpponentStates(self):
		player_states = [
			setup.NewPlayerState()._replace(gems=[gems.RED]),
			setup.NewPlayerState()._replace(gems=[gems.BLUE]),
			setup.NewPlayerState()._replace(gems=[gems.GREEN]),
			setup.NewPlayerState()._replace(gems=[gems.WHITE]),
		]
		game_state = setup.SinglePlayerEmptyGameState()._replace(
			player_states=player_states,
			turn=1
		)
		state = player_game_state.PlayerGameState(
			game_state, game_rules.GAME_RULES)
		opponent_gems = []
		for opp in state.opponent_states:
			opponent_gems.append(gem_utils.GetGems(opp.gem_counts)[0])
		expected_opponent_gems = [
			player_states[2].gems[0],
			player_states[3].gems[0],
			player_states[0].gems[0],
		]
		self.assertEquals(opponent_gems, expected_opponent_gems)


if __name__ == "__main__":
	unittest.main()
