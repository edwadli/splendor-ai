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

  def RunIterative(self):
    """Yields a list of GameResults."""
    results = []
    for agent_set in itertools.combinations(
        self._ids_to_agent_class.keys(), self._num_players):
      for agent_ordering in itertools.permutations(agent_set):
        agents = [
          self._ids_to_agent_class[agent_id]() for agent_id in agent_ordering]
        game_driver = driver.Driver(agents, gamebox.GAMEBOX)
        winners = game_driver.RunGame(early_stop_round=1000)
        results.append(GameResult(
            agent_ids=agent_ordering,
            winners=winners,
            final_game_state=game_driver.game_state,
            num_turns_played=game_driver.num_rounds_played))
        yield results

  def Run(self):
    results = []
    for intermediate in self.RunIterative():
      results = intermediate
    return results
