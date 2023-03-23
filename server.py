from flask import Flask, request, jsonify
from game import Game
import uuid

class Server:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.add_url_rule('/api/create_game', 'create_game', self.create_game, methods=['POST'])
        self.app.add_url_rule('/api/join_game', 'join_game', self.join_game, methods=['POST'])
        self.app.add_url_rule('/api/update_game', 'update_game', self.update_game, methods=['POST'])
        self.app.add_url_rule('/api/get_game_state', 'get_game_state', self.get_game_state, methods=['GET'])
        self.app.add_url_rule('/api/reset_game', 'reset_game', self.reset_game, methods=['POST'])

        self.game = Game()

        tokens = {}

    def start_server(self):
        self.app.run(host='0.0.0.0', port='5742')

    def create_game(self):
        self.game = Game()
        return jsonify({'status': 'Game created'})

    def join_game(self, game_id):
        if self.game is not None:
#            player_id = self.game.add_player()
            token = uuid.uuid4().hex
            self.tokens[token] = player_id
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Game does not exist'}), 404

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
