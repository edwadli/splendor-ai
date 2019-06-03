from src.proto.gem_proto import GemType
from src.proto.player_action_proto import PlayerAction

PLAYER_ACTION = PlayerAction(
        gems_taken={
                GemType.BLUE: 1,
                GemType.GREEN: 1,
                GemType.BROWN: 1},
        gems_returned={},
        purchased_card_id=0,
        reserved_card_id=0,
        topdeck_level=0,
        noble_tile_id=0
        )
        

