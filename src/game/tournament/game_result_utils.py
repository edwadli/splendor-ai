"""Utils for computing stats from GameResults."""

import collections


def GetWinStats(game_results):
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


def NumTerminatedGames(game_results):
  """Returns the number of terminated games."""
  count = 0
  for game_result in game_results:
    if len(game_result.winners) == 0:
      count += 1
  return count


def GetTurnStats(game_results):
  """Returns a histogram of game lengths (in rounds played)."""
  hist = collections.Counter()
  for game_result in game_results:
    hist[game_result.num_rounds_played] += 1
  return hist


def GetWinsByPositionStats(game_results):
  """Returns a histogram of wins by seat position."""
  hist = collections.Counter()
  for game_result in game_results:
    for winner_idx in game_result.winners:
      hist[winner_idx] += 1
  return hist
