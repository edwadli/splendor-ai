"""Tests for player.py"""

import unittest

from src.data import gems
from src.game import player
from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard
from src.proto.gem_proto import GemType
from src.proto.noble_tile_proto import NobleTile
from src.proto.player_state_proto import PlayerState


class FakePlayer(player.Player):
	def PlayTurn(player_game_state):
		pass


class TestPlayer(unittest.TestCase):

	def test_Player(self):
		dev_card = DevelopmentCard(
			asset_id="1234",
			level=Deck.LEVEL_2,
			points=3,
			gem=gems.RED,
			cost=[gems.RED] * 6)
		noble_tile = NobleTile(
			asset_id="4321",
			points=3,
			gem_type_requirements=(
				[GemType.RED] * 4 +
				[GemType.WHITE] * 4))
		player_state = PlayerState(
			gems=[
				gems.BLUE,
				gems.RED,
				gems.BLUE,
			],
			purchased_cards=[dev_card, dev_card],
			unhidden_reserved_cards=[dev_card],
			hidden_reserved_cards=[dev_card],
			noble_tiles=[],
		)

		result = FakePlayer(player_state)
		self.assertEquals(result.player_state, player_state)
		self.assertEquals(result.gem_counts,
			{GemType.BLUE: 2, GemType.RED: 1})
		self.assertEquals(result.reserved_cards, [dev_card, dev_card])
		self.assertEquals(result.num_purchased_cards, 2)
		self.assertEquals(result.num_points, 6)
		self.assertEquals(result.gem_discounts, {GemType.RED: 2})


if __name__ == "__main__":
	unittest.main()
