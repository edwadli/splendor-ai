"""Agent implementation for interactive demo."""

from src.game import agent
from src.proto.player_action_proto import PlayerAction

class CliAgent(agent.Agent):
  """An agent that queries the user for a game action."""
  def PlayTurn(self, player_game_state):
    """Returns a PlayerAction based on CLI input."""
    # TODO: parse input from CLI
    print self._ActionOptions(player_game_state)
    user_input = raw_input()
    player_action = PlayerAction(
        gems_taken=[],
        gems_returned=[],
        purchased_card_id="0000",
        reserved_card_id="0000",
        topdeck_level="0000",
        noble_tile_id="0000")
    return player_action

  def _ActionOptions(self, player_game_state):
    msg = "Options: \n"
    # TODO: display menu options
    msg += "Pass"
    return msg
