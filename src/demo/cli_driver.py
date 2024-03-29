"""Driver implementation for interactive demo."""

from src.demo import cli_utils
from src.game import driver
from src.game import gem_utils
from src.game import player_game_state


class CliDriver(driver.Driver):
  """A game driver that prints turns and game state."""
  def RunGame(self):
    print(self._IntroMessage())
    while True:
      _ = input()
      winners = self.GetWinners()
      if winners:
        print(self._WinnerMessage(winners))
        return winners
      else:
        print(self._GameStateMessage())
        print(self._TurnMessage())
        player_action = self.RunNextTurn()
        print(self._PlayerActionMessage(player_action))

  def _IntroMessage(self):
    msg = "==============================\n\n\n"
    msg += "Splendid: "
    msg += str(len(self.game_state.player_states)) + " players"
    msg += "\n==============================\n\n\n"
    return msg

  def _WinnerMessage(self, winners):
    msg = ""
    if len(winners) == 1:
      msg += "Player "
    else:
      msg += "Players "
    msg += str(winners)
    msg += " won"
    return msg  

  def _TurnMessage(self):
    return "Player " + str(self.game_state.turn) + "'s turn:"

  def _PlayerActionMessage(self, player_action):
    msg = ""
    msg += "Taking: " + cli_utils.GemsAsString(player_action.gems_taken, ", ") + "\n"
    msg += "Return: " + cli_utils.GemsAsString(player_action.gems_returned, ", ") + "\n"
    if player_action.purchased_card_id is not None:
      msg += "Purchase: " + player_action.purchased_card_id + "\n"
    if player_action.reserved_card_id is not None:
      msg += "Reserve: " + player_action.reserved_card_id + "\n"
    if player_action.topdeck_level is not None:
      msg += "Reserve: " + cli_utils.DeckAsString(player_action.topdeck_level) + "\n"
    if player_action.noble_tile_id is not None:
      msg += "Noble: " + player_action.noble_tile_id + "\n"
    return msg

  def _GameStateMessage(self):
    msg = "Board:\n"
    msg += "Gems:\n"
    msg += cli_utils.GemsAsString(self.game_state.available_gems)
    msg += "\n\n"
    msg += "Cards:\n"
    msg += cli_utils.CardsByDeckAsString(
        self.game_state.development_cards, self.game_rules)
    msg += "Nobles:\n"
    msg += cli_utils.NoblesAsString(self.game_state.noble_tiles)
    return msg
