from flask import Flask, request
from parser import gameParser

api = Flask(__name__)


@api.route('/', methods=['GET'])
def index():
  return "Example request: /game?url=http://www.sajl.org/images/tilastot/crocodiles-butchers-21-05-2022.shtml. Find games to parse from here: http://www.sajl.org/selaus/otteluohjelma.php?sarja=1&kausi=2022"

@api.route('/game', methods=['GET'])
def get_game_stats():
  args = request.args
  gameUrl = args.get("gameUrl", default="http://www.sajl.org/images/tilastot/roosters-steelers-14-05-2022.shtml", type=str)
  return gameParser(gameUrl)

if __name__ == '__main__':
    api.run() 