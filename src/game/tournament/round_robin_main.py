"""Runs a round robin tournament."""

from src.game.tournament import round_robin
from src.game.tournament import game_result_utils
from src.agents.naive import greedy_buy_bot


AGENT_CLASSES = {
  "agent_1": greedy_buy_bot.GreedyBuyBot,
  "agent_2": greedy_buy_bot.GreedyBuyBot,
  "agent_3": greedy_buy_bot.GreedyBuyBot,
  "agent_4": greedy_buy_bot.GreedyBuyBot,
}

NUM_PLAYERS = 4

def RunRoundRobin():
  print ("Running round robin tournament (" +
         str(NUM_PLAYERS) + " player games) with:")
  print "\n".join(AGENT_CLASSES.keys()) + "\n"
  print "..."
  round_robin_runner = round_robin.RoundRobinRunner(
      AGENT_CLASSES, num_players=NUM_PLAYERS)
  results = round_robin_runner.Run()
  print "Games finished. Producing report:\n"
  print "================================\n"
  scores = game_result_utils.GetWinStats(results)
  for agent_id, num_wins in scores.iteritems():
    print agent_id + ":\t" + str(num_wins)
  print "================================\n"


if __name__ == "__main__":
  RunRoundRobin()
