from flask import Flask, request, jsonify
from game import Game
import uuid
from threading import Thread
import random
import time


def update_skeletal_state(game):
    while True:
        num = random.randint(1,100)
        game.update_state(num)
        time.sleep(5)

class Server:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.add_url_rule('/api/create_game', 'create_game', self.create_game, methods=['POST'])
        self.app.add_url_rule('/api/join_game', 'join_game', self.join_game, methods=['POST'])
        self.app.add_url_rule('/api/update_game', 'update_game', self.update_game, methods=['POST'])
        self.app.add_url_rule('/api/get_game_state', 'get_game_state', self.get_game_state, methods=['GET'])
        self.app.add_url_rule('/api/reset_game', 'reset_game', self.reset_game, methods=['POST'])
        self.app.add_url_rule('/api/make_suggestion', 'make_suggestion', self.make_suggestion, methods=['POST'])
        self.app.add_url_rule('/api/make_accusation', 'make_accusation', self.make_accusation, methods=['POST'])
        self.game = Game()

        tokens = {}
        self.t = Thread(target=update_skeletal_state, args=(self.game,))
        self.t.start()

    def start_server(self):
        self.app.run(host='0.0.0.0', port='5742')

    def create_game(self):
        self.game = Game()
        return jsonify({'status': 'Game created'})

    def make_suggestion(self):
        suggestion = request.json
        print("Server got suggestion: " + str(request.json))
        return jsonify({'state': self.game.make_suggestion("player", suggestion)})

    # accuse a player
    def make_accusation(self):
        # check for a token
        token = request.headers.get('Authorization')
        if token in self.tokens:
            # get json and session id
            data = request.get_json()
            player_id = self.tokens[token]
            print("Server got accusation: " + str(request.json))

            # try to accuse a player and return a cooresponding stratus
            if self.game.accuse(player_id, data["character"], data["weapon"], data["room"]):
                return jsonify({'status': 'Success, you won the game'})
            else:
                return jsonify({'status': 'Failure, your guess was wrong'})
        else:
            return jsonify({'error': 'Unauthorized'}), 401

    # adds a player to a game with a username
    def join_game(self, game_id):
        if self.game is not None:
            # get data and add a player
            data = request.get_json()
            player_id = self.game.add_player(data["username"])

            # create a token based on the session id
            token = uuid.uuid4().hex
            self.tokens[token] = player_id
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Game does not exist'}), 404
    
    # set a character
    def set_character(self):
        # check for a token
        token = request.headers.get('Authorization')
        if token in self.tokens:
            # get data and session id
            data = request.get_json()
            player_id = self.tokens[token]

            # try to set a character
            if self.game.set_character(player_id, data["character"]):
                return jsonify({'status': 'Success'})
            else:
                return jsonify({'status': 'Failed, character in use'})
        else:
            return jsonify({'error': 'Unauthorized'}), 401


    def update_game(self):
        token = request.headers.get('Authorization')
        if token in self.tokens:
            player_id = self.tokens[token]
            data = request.get_json()
#            self.game.update_game(data)
            return jsonify({'status': 'Success'})
        else:
            return jsonify({'error': 'Unauthorized'}), 401

    def get_game_state(self):
        if self.game is not None:
            print("hit")
            state, data = self.game.get_state()
            return jsonify({'state': state, 'data': data})
        else:
            return jsonify({'error': 'Game not created'}), 404

    def reset_game(self):
        token = request.headers.get('Authorization')
        if token in self.tokens:
#            self.game.reset_game()
            return jsonify({'status': 'Success'})
        else:
            return jsonify({'error': 'Unauthorized'}), 401

def main():
    """ Main entry point of the app """
    print("you have run the server from your command line")
    server = Server()
    server.start_server()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
