"""Orchestrator for running the game."""

from src.game import agent
from src.game import engine
from src.game import player_game_state
from src.game import setup

class Driver(object):
	"""Orchestrates the game states and agents.

	Either 'gamebox' xor ('game_state' AND 'game_rules') must be
	specified. If not, ValueError is raised.
	Additionally, note that random_seed can only be specified if
	'gamebox' is specified.
	
	Params:
		agents: A list of Agents.
		gamebox: A Gamebox for initializing the game. If specified,
			both 'game_state' and 'game_rules' must be None.
		random_seed: Random seed for initializing game state from
			'gamebox'. Can only be specified if 'gamebox' is specified.
		game_state: A GameState for initializing the game. If
			specified, 'game_rules' must also be specified, and both
			'gamebox' and 'random_seed' must be None. Assumes that the
			value is a valid GameState consistent with 'game_rules'.
		game_rules: A GameRules for running the game. If specified,
			'game_state' must also be specified and 'gamebox' must be
			None. Assumes that value is consistent with 'game_state'.
	Raises:
		ValueError: Invalid combination of input values for
			initializing the game.
		TypeError: The agents are not Agent type.
		IndexError: The number of agents does not match the number of
			player states.
	"""
	def __init__(self, agents, gamebox=None, random_seed=None,
				 game_state=None, game_rules=None):
		# Initialize game state.
		self._agents = agents
		if (gamebox is not None and
			game_state is None and game_rules is None):
			self._game_state = setup.InitializeGameState(
				gamebox, len(self._agents), random_seed)
			self._game_rules = gamebox.game_rules
		elif (gamebox is None and random_seed is None and
			  game_state is not None and game_rules is not None):
			self._game_state = game_state
			self._game_rules = game_rules
		else:
			raise ValueError("Invalid driver initialization inputs")
		
		player_states = self._game_state.player_states
		if (len(self._agents) != len(player_states)):
			raise IndexError(
				"Number of agents and player states don't match")
		# Verify agents are Players.
		for player_agent in self._agents:
			if not isinstance(player_agent, agent.Agent):
				raise TypeError("Agents must be of type Agent")

	def RunNextTurn(self):
		"""Returns the next agent's PlayerAction and updates the game state."""
		turn = self._game_state.turn
		agent_to_play = self._agents[turn]
		game_view = player_game_state.PlayerGameState(self._game_state)
		# Get the agent's PlayerAction for this turn.
		player_action = agent_to_play.PlayTurn(game_view)
		# TODO: check if player_action is valid.
		if False:
			raise ValueError(
				"Agent " + str(turn) + "'s PlayerAction is invalid")
		# TODO: update game state with player_action.
		self._game_state = self._game_state
		self._game_state._replace(turn=turn + 1 % len(self._agents))
		return player_action

	def GetWinners(self):
		"""Returns the indices of the winners (as a tuple).
		
		If the returned tuple is empty, then RunAgentTurn()
		should be called to continue the play of game.
		"""
		if self._game_state.turn != 0:
			return tuple()  # only check for winner after a full round
		scores = []
		for player_state in self._game_state.player_states:
			num_points = player_game_state.CountPoints(player_state)
			num_cards = len(player_state.purchased_cards)
			# Tiebreak with the fewest cards purchased. We make
			# 'num_cards' negative here to take advantage of max().
			scores.append((num_points, -num_cards))
		winning_score = max(scores)
		if winning_score[0] < self._game_rules.points_to_win:
			return tuple()
		# Get all candidates with the winning score.
		winners = tuple(
			i for i, score in enumerate(scores)
			if score == winning_score)
		return winners

	def RunGame(self):
		"""Returns the winning agents' indices."""
		while True:
			winners = self.GetWinners()
			if winners:
				return winners
			else:
				_ = self.RunNextTurn()

	@property
	def game_state(self):
		return self._game_state
