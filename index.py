from flask import Flask, json
from parser import gameParser

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/game', methods=['GET'])
def get_companies():
  return json.dumps(gameParser())

if __name__ == '__main__':
    api.run() 