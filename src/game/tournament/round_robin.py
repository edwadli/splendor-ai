"""Runner for a round robin of bots."""

import itertools

from src.data import gamebox
from src.game import driver
from src.game import driver
from src.proto.game_result_proto import GameResult


class RoundRobinRunner(object):
  """Runs a round robin tournament given a list of agents."""
  def __init__(self, ids_to_agent_class, num_players=4):
    self._ids_to_agent_class = ids_to_agent_class
    self._num_players = num_players

  def Run(self):
    """Returns a list of GameResults."""
    results = []
    for agent_set in itertools.combinations(
        self._ids_to_agent_class.keys(), self._num_players):
      for agent_ordering in itertools.permutations(agent_set):
        agents = [
          self._ids_to_agent_class[agent_id]() for agent_id in agent_ordering]
        game_driver = driver.Driver(agents, gamebox.GAMEBOX)
        winners = driver.RunGame()
        results.append(GameResult(
            agent_ids=agent_ordering,
            winners=winners,
            final_game_state=driver.game_state,
            num_turns_played=driver.num_turns_played))
    return results
