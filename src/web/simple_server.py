"""A simply splendid webserver."""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json


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
    post_data = self.rfile.read(content_length)

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

    result_data = json.loads(post_data)
    self.wfile.write(json.dumps(data))


def run_server(server_class=HTTPServer, handler_class=GameDriverHandler,
               port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting server...'
    httpd.serve_forever()


if __name__ == "__main__":
  run_server()
