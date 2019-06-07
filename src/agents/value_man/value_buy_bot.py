"""A bot that reserves high-value cards."""

from src.game import agent


class ValueBuyBot(agent.Agent):
  """An agent that tries to prioritize high value cards."""
  def PlayTurn(self, player_game_state):
    pass
