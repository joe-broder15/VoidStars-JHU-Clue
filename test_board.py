import unittest
from board import Board, RoomEnum, RoomType
from room import Room


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_functionality(self):
        # Test that characters can move through passages
        self.board.start_board(character_names=["Miss Scarlett", "Colonel Mustard"])

        print("\n\nThe position for the room with name KITCHEN is ", self.board.get_room_name_position("KITCHEN"), "")
        print("The position for the room with name HALLWAY_LOUNGE_DINING is ",
              self.board.get_room_name_position("HALLWAY_LOUNGE_DINING"), "\n\n")

        print(f"Assert Miss Scarlett is in HALLWAY_STUDY_LIBRARY")
        self.assertEqual(self.board.get_player_room("Miss Scarlett"), "HALLWAY_STUDY_LIBRARY")
        print(f"Move Miss Scarlett to RoomEnum.STUDY")

        print("--------")
        print(self.board.get_ascii_board())
        print("--------")

        self.board.move_player("Miss Scarlett", "STUDY")
        print(f"Assert Miss Scarlett is in HALLWAY_STUDY")

        self.assertEqual(self.board.get_player_room("Miss Scarlett"), "STUDY")
        self.board.move_player("Miss Scarlett", "KITCHEN")
        print(f"Assert Miss Scarlett is in KITCHEN")

        self.assertEqual(self.board.get_player_room("Miss Scarlett"), "KITCHEN")

        print("Miss Scarlett's valid moves are ", self.board.get_valid_moves("Miss Scarlett"))
        print(self.board.get_state())
        print("--------")
        print(self.board.get_ascii_board())
        print("--------")

if __name__ == '__main__':
    unittest.main()
