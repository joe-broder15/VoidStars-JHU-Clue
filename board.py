from enum import Enum
from room import Room

class RoomType(Enum):
        NORMAL = 1
        PASSAGE = 2

class Board:
#Dict containing each room's name, type, and connections
ROOM_DATA = {
    RoomEnum.KITCHEN: {'name': 'Kitchen', 'type': RoomType.NORMAL, 'connections': [RoomEnum.BALLROOM, RoomEnum.PASSAGEWAY_STUDY_KITCHEN]},
    RoomEnum.BALLROOM: {'name': 'Ballroom', 'type': RoomType.NORMAL, 'connections': [RoomEnum.KITCHEN, RoomEnum.CONSERVATORY, RoomEnum.BILLIARD_ROOM, RoomEnum.DINING_ROOM]},
    RoomEnum.CONSERVATORY: {'name': 'Conservatory', 'type': RoomType.NORMAL, 'connections': [RoomEnum.BALLROOM, RoomEnum.PASSAGEWAY_CONSERVATORY_LOUNGE]},
    RoomEnum.BILLIARD_ROOM: {'name': 'Billiard Room', 'type': RoomType.NORMAL, 'connections': [RoomEnum.BALLROOM, RoomEnum.LIBRARY, RoomEnum.HALL]},
    RoomEnum.LIBRARY: {'name': 'Library', 'type': RoomType.NORMAL, 'connections': [RoomEnum.BILLIARD_ROOM, RoomEnum.STUDY]},
    RoomEnum.STUDY: {'name': 'Study', 'type': RoomType.NORMAL, 'connections': [RoomEnum.LIBRARY, RoomEnum.HALL, RoomEnum.PASSAGEWAY_STUDY_KITCHEN]},
    RoomEnum.HALL: {'name': 'Hall', 'type': RoomType.NORMAL, 'connections': [RoomEnum.STUDY, RoomEnum.BILLIARD_ROOM, RoomEnum.LOUNGE]},
    RoomEnum.LOUNGE: {'name': 'Lounge', 'type': RoomType.NORMAL, 'connections': [RoomEnum.HALL, RoomEnum.DINING_ROOM, RoomEnum.PASSAGEWAY_CONSERVATORY_LOUNGE]},
    RoomEnum.DINING_ROOM: {'name': 'Dining Room', 'type': RoomType.NORMAL, 'connections': [RoomEnum.LOUNGE, RoomEnum.BALLROOM]},
    RoomEnum.PASSAGEWAY_STUDY_KITCHEN: {'name': 'Passageway (Study-Kitchen)', 'type': RoomType.PASSAGE, 'connections': [RoomEnum.STUDY, RoomEnum.KITCHEN]},
    RoomEnum.PASSAGEWAY_CONSERVATORY_LOUNGE: {'name': 'Passageway (Conservatory-Lounge)', 'type': RoomType.PASSAGE, 'connections': [RoomEnum.CONSERVATORY, RoomEnum.LOUNGE]},
}

    def __init__(self):
        self.rooms = []
        self.start_board()

    def add_room(self, room_id, room):
        self.rooms[room_id] = room

    def move_player(self, character, location):
        if self.check_valid_move(character, location):
            old_room = self.get_player_position(character)
            if old_room is not None:
                old_room.remove_character(character)
            location.add_character(character, location.name)

    def check_valid_move(self, character, location):
        current_room = self.get_player_position(character)
        if current_room is not None:
            return current_room.can_travel_to(location)
        return False

    def get_valid_moves(self, character):
        current_room = self.get_player_position(character)
        if current_room is not None:
            return list(current_room.travel_options)
        return []

    def get_player_position(self, character):
        for room_id, room in self.rooms.items():
            if character in room.characters:
                return room
        return None

    def start_board(self):
        for room_enum, room_info in self.ROOM_DATA.items():
            room = Room(room_info['name'], room_info['type'])
            self.add_room(room_enum, room)

        # Populate connections and room locations
        # First, add_connection automatically adds its entrance as a location within the room
        for room_enum, room_info in self.ROOM_DATA.items():
            for connection_enum in room_info['connections']:
                self.rooms[room_enum].add_connection(self.rooms[connection_enum])
        # Then add the name of the room as a location for the room's "main area"
        for room in self.rooms.values():
            room.travel_options.add(room.name)

    def get_state(self):
        return [[room.get_state() for room in row] for row in self.rooms]

    def get_room_type(self, location):
        for row in self.rooms:
            for room in row:
                if room == location:
                    return room.type
        return None

