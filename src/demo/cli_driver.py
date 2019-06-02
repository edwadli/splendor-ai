"""Driver implementation for interactive demo."""

from src.game import driver

class CliDriver(driver.Driver):
  """A game driver that prints turns and game state."""
  def RunGame(self):
    print self._IntroMessage()
    while True:
      winners = self.GetWinners()
      if winners:
        print self._WinnerMessage(winners)
        return winners
      else:
        print self._GameStateMessage()
        print self._TurnMessage()
        player_action = self.RunNextTurn()
        print self._PlayerActionMessage(player_action)

  def _IntroMessage(self):
    msg = "Splendid: "
    msg += str(len(self.game_state.player_states)) + " players"
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
    msg = str(player_action)
    return msg

  def _GameStateMessage(self):
    msg = str(self.game_state)
    return msg
