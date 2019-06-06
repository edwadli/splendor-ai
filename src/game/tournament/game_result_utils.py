"""Utils for computing stats from GameResults."""


def GetWinStats(self, game_results):
  """Returns a dict from agent ids to number of wins."""
  stats = {}
  for game_result in game_results:
    for agent_id in game_result.agent_ids:
      stats[agent_id] = 0

  for game_result in game_results:
    winning_agents = [
        game_result.agent_ids[i] for i in game_result.winners]
    for agent_id in winning_agents:
      stats[agent_id] += 1

  return stats
