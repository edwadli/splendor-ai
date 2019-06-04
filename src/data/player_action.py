import collections

from src.proto.gem_proto import GemType
from src.proto.player_action_proto import PlayerAction

PLAYER_ACTION = PlayerAction(
        gems_taken=collections.Counter({
                GemType.BLUE: 1,
                GemType.GREEN: 1,
                GemType.BROWN: 1}),
        gems_returned=collections.Counter(),
        purchased_card_id=None,
        reserved_card_id=None,
        topdeck_level=None,
        noble_tile_id=None
        )
