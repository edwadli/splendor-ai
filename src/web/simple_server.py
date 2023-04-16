"""A simply splendid webserver."""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

from src.data import gamebox
from src.game import driver
from src.game import setup
from src.proto.game_state_proto import GameState
from src.proto.player_action_proto import PlayerAction


def ParseGameState(game_state_dict):
  pass  # TODO


def GameStateAsDict(game_state):
  pass  # TODO


class GameDriverHandler(BaseHTTPRequestHandler):
  """Request handler for playing the game."""
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    with open("./src/web/html/index.html", "r") as content_file:
      content = content_file.read()
    self.wfile.write(content)

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_raw_data = self.rfile.read(content_length)
    try:
      post_data = json.loads(post_raw_data)
    except:
      self.send_error(404, "Posted data malformed.")
      return
    if "game_state" in post_data:
      try:
        game_state = ParseGameState(post_data["game_state"])
      except:
        self.send_error(404, "GameState data malformed.")
        return
    else:
      game_state = None
    if "player_action" in post_data:
      try:
        player_action = PlayerAction(**post_data["player_action"])
      except:
        self.send_error(404, "PlayerAction data malformed.")
        return
    else:
      player_action = None

    response = {}
    if game_state is None:
      if player_action is None:
        # Return a fresh game state.
        response["game_state"] = GameStateAsDict(
            setup.InitializeGameState(gamebox.GAMEBOX, num_players=4))
      else:
        self.send_error(404, "Cannot specify PlayerAction without GameState")
        return
    else:
      if player_action is None:
        # TODO: Run an opponent agent.
        pass
      else:
        # TODO: Update game state.
        pass

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(response))


def run_server(server_class=HTTPServer, handler_class=GameDriverHandler,
               port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == "__main__":
  run_server()
