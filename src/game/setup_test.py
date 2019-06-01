"""Tests for setup.py"""

import unittest

# TODO: use test data instead of real gamebox itself.
from src.data import gamebox
from src.data import gems
from src.game import setup
from src.proto.deck_proto import Deck
from src.proto.game_state_proto import GameState


class TestSetup(unittest.TestCase):

	def _AssertAllDecksExist(self, game_state):
		expected_decks = set([Deck.LEVEL_1, Deck.LEVEL_2, Deck.LEVEL_3])
		self.assertEquals(
			set(game_state.development_cards.keys()),
			expected_decks)
		for level in expected_decks:
			cards = game_state.development_cards[level]
			self.assertGreater(len(cards), 0)
			for card in cards:
				self.assertEquals(card.level, level)

	def _AssertNumberNobles(self, game_state, num_players):
		self.assertEquals(len(game_state.noble_tiles), num_players + 1)

	def _AssertPlayerStates(self, game_state, num_players):
		self.assertEquals(len(game_state.player_states), num_players)
		for player_state in game_state.player_states:
			self.assertEquals(player_state, setup.NewPlayerState())
		self.assertEquals(game_state.turn, 0)

	def test_InitializeGameStateFourPlayers(self):
		num_players = 4
		game_state = setup.InitializeGameState(
			gamebox.GAMEBOX, num_players, random_seed=0)
		
		# Check that all gems are used.
		self.assertEquals(sorted(game_state.available_gems),
			[gems.BLUE] * 7 +
			[gems.GREEN] * 7 +
			[gems.RED] * 7 +
			[gems.WHITE] * 7 +
			[gems.BROWN] * 7 +
			[gems.GOLD] * 5)
		self._AssertAllDecksExist(game_state)
		self._AssertNumberNobles(game_state, num_players)
		self._AssertPlayerStates(game_state, num_players)

	def test_InitializeGameStateThreePlayers(self):
		num_players = 3
		game_state = setup.InitializeGameState(
			gamebox.GAMEBOX, num_players, random_seed=0)
		
		# Check that all gems are used.
		self.assertEquals(sorted(game_state.available_gems),
			[gems.BLUE] * 5 +
			[gems.GREEN] * 5 +
			[gems.RED] * 5 +
			[gems.WHITE] * 5 +
			[gems.BROWN] * 5 +
			[gems.GOLD] * 5)
		self._AssertAllDecksExist(game_state)
		self._AssertNumberNobles(game_state, num_players)
		self._AssertPlayerStates(game_state, num_players)

	def test_InitializeGameStateTwoPlayers(self):
		num_players = 2
		game_state = setup.InitializeGameState(
			gamebox.GAMEBOX, num_players, random_seed=0)
		
		# Check that all gems are used.
		self.assertEquals(sorted(game_state.available_gems),
			[gems.BLUE] * 4 +
			[gems.GREEN] * 4 +
			[gems.RED] * 4 +
			[gems.WHITE] * 4 +
			[gems.BROWN] * 4 +
			[gems.GOLD] * 5)
		self._AssertAllDecksExist(game_state)
		self._AssertNumberNobles(game_state, num_players)
		self._AssertPlayerStates(game_state, num_players)

	def test_InitializeGameStateTooManyPlayers(self):
		num_players = 5
		with self.assertRaises(NotImplementedError):
			game_state = setup.InitializeGameState(
				gamebox.GAMEBOX, num_players, random_seed=0)

	def test_InitializeGameStateTooFewPlayers(self):
		num_players = 1
		with self.assertRaises(NotImplementedError):
			game_state = setup.InitializeGameState(
				gamebox.GAMEBOX, num_players, random_seed=0)


if __name__ == "__main__":
	unittest.main()