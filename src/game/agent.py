"""Interface for agents."""

import abc

class Agent(object):
  """Base abstract class for agents."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def PlayTurn(self, player_game_state):
    """Returns a PlayerAction given the PlayerGameState."""
    raise NotImplementedError("No implementation for PlayTurn method.")
