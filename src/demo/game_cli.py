"""Runs a demo game."""

from src.data import gamebox
from src.demo import cli_agent
from src.demo import cli_driver

def _SetupGame():
  agents = [cli_agent.CliAgent(), cli_agent.CliAgent()]
  driver = cli_driver.CliDriver(agents, gamebox.GAMEBOX)
  return driver

def _Main():
  while True:
    driver = _SetupGame()
    driver.RunGame()
    user_input = raw_input("Play again? Y/N")
    if user_input.lower() != "y":
      break


if __name__ == "__main__":
	_Main()
