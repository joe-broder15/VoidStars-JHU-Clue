from flask import Flask, request, jsonify
from game import Game

class Server:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.add_url_rule('/api/create_game', 'create_game', self.create_game, methods=['POST'])
        self.app.add_url_rule('/api/join_game', 'join_game', self.join_game, methods=['POST'])
        self.app.add_url_rule('/api/update_game', 'update_game', self.update_game, methods=['POST'])
        self.app.add_url_rule('/api/get_game_state', 'get_game_state', self.get_game_state, methods=['GET'])
        self.app.add_url_rule('/api/reset_game', 'reset_game', self.reset_game, methods=['POST'])

    def start_server(self):
        self.app.run

    def create_game(self):
        pass

    def join_game(self, game_id):
        pass

    def update_game(self, game_id, data):
        pass

    def get_game_state(self, game_id):
        pass

    def reset_game(self, game_id):
        pass

def main():
    """ Main entry point of the app """
    print("you have run the server from your command line")
    server = Server()
    server.start_server()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
