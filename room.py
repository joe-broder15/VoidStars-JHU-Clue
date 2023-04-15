class Room:
    def __init__(self, name, room_type, row=None, col=None):
        self.name = name
        self.row = row
        self.col = col
        self.characters = set()
        self.type = room_type
        self.travel_options = set()

    def can_travel_to(self, destination):
        return destination in self.travel_options

    def add_character(self, character):
        print(f"Adding character {character} to room {self.name} at ({self.row},{self.col})")
        self.characters.add(character)

    def remove_character(self, character):
        self.characters.pop()
        print(f"removed {character} from {self}!")

    def contains_character(self, character):
        return character in self.characters

    def get_state(self):
        return {
            'name': self.name,
            'characters': list(self.characters),
            'type': int(self.type),
            'travel_options': list(self.travel_options),
            'location': (self.row, self.col)
        }
