"""Runs a round robin tournament."""

from src.game.tournament import round_robin
from src.game.tournament import game_result_utils
from src import agents


AGENT_CLASSES = {
  # "some agent": agents.NaiveAgent,
}


def RunRoundRobin():
  print ("Running round robin tournament (" +
         str(num_players) + " player games) with:")
  print "\n".join(AGENT_CLASSES.keys()) + "\n"
  print "..."
  round_robin_runner = round_robin.RoundRobinRunner(
      AGENT_CLASSES, num_players=4)
  results = round_robin_runner.Run()
  print "Games finished. Producing report:\n"
  print "================================\n"
  scores = game_result_utils.GetWinStats(results)
  for agent_id, num_wins in scores:
    print agent_id + ":\t" + str(num_wins)
  print "================================\n"


if __name__ == "__main__":
  RunRoundRobin()
