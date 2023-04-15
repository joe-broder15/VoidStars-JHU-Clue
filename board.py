from enum import Enum
from room import Room


class RoomType(Enum):
    NORMAL = 1
    TILE = 2
    HALLWAY = 3
    WALL = 4


class RoomEnum(Enum):
    KITCHEN = (0, "Kitchen", RoomType.NORMAL, ["STUDY"])
    BALLROOM = (1, "Ballroom", RoomType.NORMAL, [])
    CONSERVATORY = (2, "Conservatory", RoomType.NORMAL, ["LOUNGE"])
    BILLIARD_ROOM = (3, "Billiard Room", RoomType.NORMAL, [])
    LIBRARY = (4, "Library", RoomType.NORMAL, [])
    STUDY = (5, "Study", RoomType.NORMAL, ["KITCHEN"])
    HALL = (6, "Hall", RoomType.NORMAL, [])
    LOUNGE = (7, "Lounge", RoomType.NORMAL, ["CONSERVATORY"])
    DINING_ROOM = (8, "Dining Room", RoomType.NORMAL, [])
    TILE = (9, "Tile", RoomType.TILE, [])
    WALL = (10, "Wall", RoomType.WALL, [])
    HALLWAY_STUDY_HALL = (11, "Hallway Study Hall", RoomType.HALLWAY, [])
    HALLWAY_HALL_LOUNGE = (12, "Hallway Hall Lounge", RoomType.HALLWAY, [])
    HALLWAY_STUDY_LIBRARY = (13, "Hallway Study Library", RoomType.HALLWAY, [])
    HALLWAY_HALL_BILLIARD = (14, "Hallway Hall Billiard Room", RoomType.HALLWAY, [])
    HALLWAY_LOUNGE_DINING = (15, "Hallway Lounge Dining Room", RoomType.HALLWAY, [])
    HALLWAY_LIBRARY_BILLIARD = (16, "Hallway Library Billiard Room", RoomType.HALLWAY, [])
    HALLWAY_BILLIARD_DINING = (17, "Hallway Billiard Room Dining Room", RoomType.HALLWAY, [])
    HALLWAY_LIBRARY_CONSERVATORY = (18, "Hallway Library Conservatory", RoomType.HALLWAY, [])
    HALLWAY_BILLIARD_BALLROOM = (19, "Hallway Billiard Room Ballroom", RoomType.HALLWAY, [])
    HALLWAY_DINING_KITCHEN = (20, "Hallway Dining Room Kitchen", RoomType.HALLWAY, [])
    HALLWAY_CONSERVATORY_BALLROOM = (21, "Hallway Conservatory Ballroom", RoomType.HALLWAY, [])
    HALLWAY_BALLROOM_KITCHEN = (22, "Hallway Ballroom Kitchen", RoomType.HALLWAY, [])

class Board:
    STARTING_LOCATIONS = [
        (1, 0),
        (3, 4),
        (1, 4),
        (4, 1),
        (0, 3),
        (1, 4)
    ]

    def __init__(self):
        self.grid_default = None
        self.characters = []
        self.character_positions = {}
        self.grid = []
        self.old_room_types = {}

    def start_board(self, character_names=None):
        self.grid_default = [
            [RoomEnum.STUDY, RoomEnum.HALLWAY_STUDY_HALL, RoomEnum.HALL, RoomEnum.HALLWAY_HALL_LOUNGE, RoomEnum.LOUNGE],
            [RoomEnum.HALLWAY_STUDY_LIBRARY, RoomEnum.WALL, RoomEnum.HALLWAY_HALL_BILLIARD, RoomEnum.WALL, RoomEnum.HALLWAY_LOUNGE_DINING],
            [RoomEnum.LIBRARY, RoomEnum.HALLWAY_LIBRARY_BILLIARD, RoomEnum.BILLIARD_ROOM, RoomEnum.HALLWAY_BILLIARD_DINING, RoomEnum.DINING_ROOM],
            [RoomEnum.HALLWAY_LIBRARY_CONSERVATORY, RoomEnum.WALL, RoomEnum.HALLWAY_BILLIARD_BALLROOM, RoomEnum.WALL, RoomEnum.HALLWAY_DINING_KITCHEN],
            [RoomEnum.CONSERVATORY, RoomEnum.HALLWAY_CONSERVATORY_BALLROOM, RoomEnum.BALLROOM, RoomEnum.HALLWAY_BALLROOM_KITCHEN, RoomEnum.KITCHEN],
        ]

        # Populate grid
        self.grid = [row[:] for row in self.grid_default]

        for x in range(len(self.grid_default)):
            for y in range(len(self.grid_default)):
                room_name = self.grid_default[x][y].value[1]
                room_type = self.grid_default[x][y].value[2]
                room_passage = self.grid_default[x][y].value[3]
                self.grid[x][y] = Room(room_name, room_type, row=x, col=y)
                # Add connecting rooms
                for room in room_passage:
                    self.grid[x][y].travel_options.add(room)

        if character_names:
            for idx, character_name in enumerate(character_names):
                row, col = self.STARTING_LOCATIONS[idx % len(self.STARTING_LOCATIONS)]
                room = self.grid[row][col]
                room.add_character(character_name)
                self.characters.append(character_name)
                self.character_positions[character_name] = (row, col)

        print(f"Started a board with {character_names}")

    def check_valid_move(self, character, new_row, new_col):
        # Check if the move is adjacent to the current position
        current_row, current_col = self.character_positions[character]
        valid_coords = [(current_row - 1, current_col), (current_row + 1, current_col),
                        (current_row, current_col - 1), (current_row, current_col + 1)]

        for passage in self.grid[current_row][current_col].travel_options:
            passage_row, passage_col = self.get_room_position(RoomEnum[passage])
            valid_coords.append((passage_row, passage_col))

        if (new_row, new_col) not in valid_coords:
            print(
                f"Invalid move for {character}: ({new_row}, {new_col}) is not adjacent to ({current_row}, {current_col})")
            return False

        # If the new position is out of bounds, return False
        if new_row < 0 or new_row >= len(self.grid) or new_col < 0 or new_col >= len(self.grid[new_row]):
            print(f"Invalid move for {character}: room is out of bounds.")
            return False

        new_room_type = self.get_room_type(new_row, new_col)

        # Check if the target position is a wall
        if new_room_type == RoomType.WALL:
            print(f"Invalid move for {character}: trying to enter a wall?")
            return False

        # Check if the target position is a tile
        if new_room_type == RoomType.TILE:
            # If the target position is occupied by another player, return False
            if ([new_row], [new_col]) in self.character_positions.values():
                print(f"Invalid move for {character}: tile is occupied")
                return False

        # If none of the above conditions are met, return True
        return True

    def get_valid_moves(self, character):
        # Get the character's coordinates on the grid, if they have any
        current_row, current_col = self.character_positions[character]
        valid_moves = []

        # If the character has coordinates on the grid, check the adjacent moves
        if current_row is not None and current_col is not None:
            # Loop through the possible directions (up, down, left, right)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Calculate the new row and column after moving in the current direction
                new_row, new_col = current_row + dr, current_col + dc
                # Check if the move is valid and add it to the valid moves list if it is
                if self.check_valid_move(character, new_row, new_col):
                    print(f"appending {(new_row, new_col)}")
                    valid_moves.append((new_row, new_col))

        for passage in self.grid[current_row][current_col].travel_options:
            passage_row, passage_col = \
                self.get_room_position(RoomEnum[passage])[0], self.get_room_position(RoomEnum[passage])[1]
            print(f"appending {passage_row, passage_col}")
            valid_moves.append((passage_row, passage_col))

        # Map the valid move coordinates to their corresponding RoomEnum names
        valid_move_names = [self.grid[row][col].name for row, col in valid_moves]

        print(f"The valid moves for {character} are {valid_move_names}")
        return valid_move_names

    def get_room_position(self, target_room_enum):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                grid_room = self.grid[row][col]
                current_room_type = grid_room.name
                target_room_type = target_room_enum.value[1]
                if current_room_type == target_room_type:
                    print(f"Room {target_room_enum} found at row {row}, col {col}.")
                    return row, col

        print(f"Room {target_room_enum} not found.")

    # Input: RoomEnum.KITCHEN
    def get_player_position(self, character):
        return self.character_positions[character][0], self.character_positions[character][1]

    def get_player_room(self, character):
        character_x = self.character_positions[character][0]
        character_y = self.character_positions[character][1]
        return self.grid_default[character_x][character_y].name

    def move_player(self, character, location_enum_name):
        # Get respective row and col
        location = getattr(RoomEnum, location_enum_name)

        row, col = self.get_room_position(location)

        if self.check_valid_move(character, row, col):
            # Get the current position of the character
            old_row, old_col = self.character_positions[character][0], self.character_positions[character][1]
            self.grid[old_row][old_col].remove_character(character)

            # Update grid
            self.grid[row][col].add_character(character)
            # Update player's position
            self.character_positions[character] = (row, col)
            print(f"Moved {character} from ({old_row, old_col}) to {row, col}")
            return True
        return False

    # Same as move_player, but doesn't validate the move.
    # Used for suggestions
    def teleport_player(self, character, location_enum_name):
        # Get respective row and col
        location = getattr(RoomEnum, location_enum_name)

        row, col = self.get_room_position(location)

        # Get the current position of the character
        old_row, old_col = self.character_positions[character][0], self.character_positions[character][1]
        self.grid[old_row][old_col].remove_character(character)

        # Update grid
        self.grid[row][col].add_character(character)
        # Update player's position
        self.character_positions[character] = (row, col)
        print(f"Moved {character} from ({old_row, old_col}) to {row, col}")
        return True

    def get_room_type(self, row, col):
        return self.grid[row][col].type

    def get_available_rooms(self, character):
        pass

    def get_state(self):
        board_state = []
        for row in self.grid:
            for cell in row:
                if cell.type != RoomType.WALL:
                    room_state = cell.get_state()
                    board_state.append(room_state)
        return board_state


if __name__ == "__main__":
    board = Board()
