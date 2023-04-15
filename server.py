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

        self.app.add_url_rule('/api/join_game', 'join_game', self.join_game, methods=['POST'])
        self.app.add_url_rule('/api/get_game_state', 'get_game_state', self.get_game_state, methods=['GET'])
        self.app.add_url_rule('/api/make_suggestion', 'make_suggestion', self.make_suggestion, methods=['POST'])
        self.app.add_url_rule('/api/make_accusation', 'make_accusation', self.make_accusation, methods=['POST'])
        self.app.add_url_rule('/api/can_suggest', 'can_suggest', self.can_suggest, methods=['GET'])
        self.game = Game()

        tokens = {}
        self.t = Thread(target=update_skeletal_state, args=(self.game,))
        self.t.start()

    def start_server(self):
        self.app.run(host='0.0.0.0', port='5742')

    # accuse a player
    def make_accusation(self):
        data = request.get_json()
        player_id = data["session_id"]
        if self.game.get_player(player_id):
            print("Server got accusation: " + str(request.json))
            # try to accuse a player and return a cooresponding stratus
            if self.game.accuse(player_id, data["character"], data["weapon"], data["room"]):
                return jsonify({'status': 'Success, you won the game'})
            else:
                return jsonify({'status': 'Failure, your guess was wrong'})
        else:
            return jsonify({'status': 'Failed, user does not exist'})

    # adds a player to a game with a username
    def join_game(self, game_id):
        # get data and add a player
        data = request.get_json()
        session_id = self.game.add_player(data["username"])
        return jsonify({'session_id': session_id})
    
    # set a character
    def set_character(self):
        # get data and session id
        data = request.get_json()
        player_id = data["session_id"]
        if self.game.get_player(player_id):
            # try to set a character
            if self.game.set_character(player_id, data["character"]):
                return jsonify({'status': 'Success'})
            else:
                return jsonify({'status': 'Failed, character in use'})
        return jsonify({'status': 'Failed, user does not exist'})
        

    def get_game_state(self):
        pass

    def make_suggestion(self):
        pass

    def can_suggest(self):
        pass

def main():
    """ Main entry point of the app """
    print("you have run the server from your command line")
    server = Server()
    server.start_server()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
