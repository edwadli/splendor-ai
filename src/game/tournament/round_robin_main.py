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


def PrintWinStats(results):
  scores = game_result_utils.GetWinStats(results)
  print "===========WINS=================\n"
  for agent_id, num_wins in scores.iteritems():
    print agent_id + ":\t" + str(num_wins)
  print "Terminated games: " + str(
      game_result_utils.NumTerminatedGames(results))
  print "================================\n"


def PrintTurnStats(results):
  hist = game_result_utils.GetTurnStats(results)
  print "=======TURN STATS===============\n"
  for num_rounds, count in hist.iteritems():
    print str(num_rounds) + ":\t" + str(count)  
  print "================================\n"


def PrintSeatPositionStats(results):
  hist = game_result_utils.GetWinsByPositionStats(results)
  print "=======POSITION STATS===========\n"
  for position in range(NUM_PLAYERS):
    print str(position) + ":\t" + str(hist[position])
  print "================================\n"


def RunRoundRobin():
  print ("Running round robin tournament (" +
         str(NUM_PLAYERS) + " player games) with:")
  print "\n".join(AGENT_CLASSES.keys()) + "\n"
  print "..."
  round_robin_runner = round_robin.RoundRobinRunner(
      AGENT_CLASSES, num_players=NUM_PLAYERS)
  results = []
  for intermediate_results in round_robin_runner.RunIterative():
    results = intermediate_results
    PrintWinStats(results)

  print "Games finished. Producing report:\n"
  PrintWinStats(results)
  PrintTurnStats(results)
  PrintSeatPositionStats(results)

  print "Terminated games:\n"
  for result in results:
    if len(result.winners) == 0:
      print str(result) + "\n"


if __name__ == "__main__":
  RunRoundRobin()
