import unittest
from board import Board, RoomEnum, RoomType
from room import Room


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_functionality(self):
        # Test that characters can move through passages

        self.board.start_board(character_names=["Colonel Mustard", "Miss Scarlett"])
        print("Kitchen is at", self.board.get_room_position(RoomEnum.KITCHEN))
        self.assertEqual(self.board.get_player_position("Miss Scarlett"), (5, 5))
        self.board.move_player("Miss Scarlett", 5, 4)
        self.assertEqual(self.board.get_player_position("Miss Scarlett"), (5, 4))
        self.assertEqual(self.board.get_player_position("Colonel Mustard"), (1, 1))
        self.board.move_player("Colonel Mustard", 0, 1)  # move to KITCHEN
        print(self.board.get_state())

        self.assertEqual(self.board.get_player_position("Colonel Mustard"), (0, 1))
        print("Valid moves for Colonel Mustard are ", self.board.get_valid_moves("Colonel Mustard"))
        self.board.move_player("Colonel Mustard", 6, 5)  # move to TILE
        self.assertEqual(self.board.get_player_position("Colonel Mustard"), (6, 5))
        self.board.move_player("Colonel Mustard", 5, 5)  # move to LOUNGE through passage
        self.assertEqual(self.board.get_player_position("Colonel Mustard"), (5, 5))
        print(self.board.get_state())

if __name__ == '__main__':
    unittest.main()