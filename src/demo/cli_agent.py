"""Agent implementation for interactive demo."""

import itertools

from src.demo import cli_utils
from src.game import agent
from src.proto.gem_proto import GemType
from src.proto.player_action_proto import PlayerAction


def AsFirstPerson(agent_cls, name="my"):
  """Returns the given agent class wrapped with first-person viewer."""
  class FirstPersonAgentWrapper(agent_cls):
    def PlayTurn(self, player_game_state):
      print name + " turn:\n"
      print "Num points: " + str(player_game_state.self_state.num_points)
      print "Reserved cards:"
      print cli_utils.CardsListAsString(player_game_state.self_state.reserved_cards)
      print "Gems:"
      print cli_utils.GemsAsString(player_game_state.self_state.gem_counts) + "\n"
      return super(FirstPersonAgentWrapper, self).PlayTurn(player_game_state)
  return FirstPersonAgentWrapper


def AsThirdPerson(agent_cls, name="opp's"):
  """Returns the given agent class wrapped with third-person viewer."""
  class ThirdPersonAgentWrapper(agent_cls):
    def PlayTurn(self, player_game_state):
      print name + " turn:\n"
      print "Num points: " + str(player_game_state.self_state.num_points)
      return super(ThirdPersonAgentWrapper, self).PlayTurn(player_game_state)
  return ThirdPersonAgentWrapper


class CliAgent(agent.Agent):
  """An agent that queries the user for a game action."""
  def PlayTurn(self, player_game_state):
    """Returns a PlayerAction based on CLI input."""
    print self._ActionOptions(player_game_state)
    while True:
      user_input = raw_input()
      player_action = self._ParseInput(user_input)
      if player_action is not None:
        break
      else:
        print "Unable to parse, try again:\n"
    return player_action

  def _ActionOptions(self, player_game_state):
    msg = "\nOptions: \n" + cli_utils.THICK_SEPARATOR
    msg += self._TakeGemsOption(player_game_state) + "\n\n"
    msg += self._BuyCardOption(player_game_state) + "\n\n"
    msg += self._ReserveCardOption(player_game_state) + "\n"
    msg += cli_utils.THICK_SEPARATOR
    return msg

  def _TakeGemsOption(self, player_game_state):
    msg = ""
    gem_counts = player_game_state.gem_counts
    num_available = sum(
        value for gem_type, value in gem_counts.iteritems()
        if gem_type != GemType.GOLD)
    if num_available == 0:
      msg += "(Can't take gems)"
      msg += cli_utils.THIN_SEPARATOR
      return msg

    gem_limit = player_game_state.GemLimit()
    # List out double taking options.
    return_num_double = max(0, 2 - gem_limit)
    msg += "Double taking options"
    if return_num_double > 0:
      msg += " (return " + str(return_num_double) + ")"
    msg += ":\n"
    for gem_type in gem_counts:
      if gem_type == GemType.GOLD:
        continue
      if player_game_state.CanTakeTwo(gem_type):
        msg += cli_utils.GemTypeToSymbol(gem_type) * 2
        msg += " " + "X" * return_num_double
        msg += "\n"
    # List out single taking options.
    return_num_singles = max(0, 3 - gem_limit)
    msg += "Single taking options"
    if return_num_singles > 0:
      msg += " (return " + str(return_num_singles) + ")"
    msg += ":\n"
    gem_types = [
        gem_type for gem_type, count in gem_counts.iteritems()
        if count > 0 and gem_type != GemType.GOLD]
    for taking_option in itertools.combinations(gem_types, 3):
      for gem_type in taking_option:
        msg += cli_utils.GemTypeToSymbol(gem_type)
      msg += " " + "X" * return_num_singles
      msg += "\n"
    msg += cli_utils.THIN_SEPARATOR
    return msg

  def _BuyCardOption(self, player_game_state):
    msg = ""
    return msg

  def _ReserveCardOption(self, player_game_state):
    msg = ""
    return msg

  def _ParseInput(self, user_input):
    player_action = PlayerAction(
        gems_taken=[],
        gems_returned=[],
        purchased_card_id="0000",
        reserved_card_id="0000",
        topdeck_level="0000",
        noble_tile_id="0000")
    return None
