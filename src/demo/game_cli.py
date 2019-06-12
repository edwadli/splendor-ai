"""Runs a demo game."""

import logging

from src.data import gamebox
from src.demo import cli_agent
from src.demo import cli_driver
from src.agents.naive import greedy_buy_bot
from src.agents.value_man import value_buy_bot


def _SetupGame():
  agents = [
      cli_agent.AsThirdPerson(greedy_buy_bot.GreedyBuyBot)(),
      cli_agent.AsThirdPerson(greedy_buy_bot.GreedyBuyBot)(),
      cli_agent.AsThirdPerson(greedy_buy_bot.GreedyBuyBot)(),
      cli_agent.AsFirstPerson(value_buy_bot.ValueBuyBot)(),
  ]
  driver = cli_driver.CliDriver(agents, gamebox.GAMEBOX)
  return driver

def _Main():
  logging.basicConfig(level=logging.DEBUG)
  while True:
    driver = _SetupGame()
    driver.RunGame()
    user_input = raw_input("Play again? Y/N")
    if user_input.lower() != "y":
      break


if __name__ == "__main__":
	_Main()
