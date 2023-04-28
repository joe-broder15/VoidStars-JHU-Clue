from flask import Flask, request, jsonify, Response
from game import Game
import uuid
from threading import Thread
import random
import time
from flask_cors import CORS

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.add_url_rule('/api/join_game', 'join_game', self.join_game, methods=['POST'])
        self.app.add_url_rule('/api/get_game_state', 'get_game_state', self.get_game_state, methods=['POST'])
        self.app.add_url_rule('/api/get_available_moves', 'get_available_moves', self.get_available_moves, methods=['GET'])
        self.app.add_url_rule('/api/get_ascii_board', 'get_ascii_board', self.get_ascii_board, methods=['GET'])
        self.app.add_url_rule('/api/make_suggestion', 'make_suggestion', self.make_suggestion, methods=['POST'])
        self.app.add_url_rule('/api/make_accusation', 'make_accusation', self.make_accusation, methods=['POST'])
        self.app.add_url_rule('/api/can_suggest', 'can_suggest', self.can_suggest, methods=['GET'])
        self.app.add_url_rule('/api/set_character', 'set_character', self.set_character, methods=['POST'])
        self.app.add_url_rule('/api/start_game', 'start_game', self.start_game, methods=['POST'])
        self.app.add_url_rule('/api/end_turn', 'end_turn', self.end_turn, methods=['POST'])
        self.app.add_url_rule('/api/move_player', 'move_player', self.move_player, methods=['POST'])
        self.game = Game()

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
    def join_game(self):
        # get data and add a player
        data = request.get_json()
        session_id = self.game.add_player(data["username"])
        return jsonify(session_id)
    
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

    def get_available_moves(self):
        # get data and session id
        data = request.get_json()
        player_id = data["session_id"]
        return jsonify({'availableMoves': self.game.get_available_moves(player_id)})

    def start_game(self):
        self.game.start_game()
        return jsonify({'status': 'Success, game started'})
    
    def end_turn(self):
        data = request.get_json()
        player_id = data["session_id"]
        self.game.end_turn(player_id)
        return {"status": "Success, player turn ended"}
    
    def move_player(self):
        data = request.get_json()
        player_id = data["session_id"]
        location = data["location"]
        if self.game.move_player(player_id, location):
            return jsonify({'status': 'Success, player moved'})
        return jsonify({'status': 'Failed, player not moved'})
        
    def get_game_state(self):
        print("hit")
        data = request.get_json()
        player_id = data["session_id"]
        if True:#self.game.get_player(player_id):
            return jsonify({"status": "success", "state":self.game.get_state(player_id)})
        else:
            return jsonify({'status': 'Failed, bad session id'})

    def get_ascii_board(self):
        ascii_board = self.game.get_ascii_board()
        return Response(ascii_board(), content_type="text/plain; charset=utf-8")

    def make_suggestion(self):
        data = request.get_json()
        player_id = data["session_id"]
        card = self.game.make_suggestion(player_id, data["character"], data["weapon"], data["location"])
        if card is None:
            return jsonify({'card': 'None'})
        else:
            return jsonify({'card': card})

    def can_suggest(self):
        data = request.get_json()
        player_id = data["session_id"]
        return jsonify({'canSuggest': self.game.can_suggest(player_id)})

def main():
    """ Main entry point of the app """
    print("you have run the server from your command line")
    server = Server()
    server.start_server()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
