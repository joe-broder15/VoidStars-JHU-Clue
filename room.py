class Room:
    def __init__(self, name, room_type, starting_character=None):
        self.name = name
        self.characters = {}
        self.type = room_type
        self.travel_options = set()
        self.connections = set()
        self.starting_character = starting_character
        self.weapon = None

    def can_travel_to(self, destination):
        return destination in self.travel_options

    def add_connection(self, connection):
        self.connections.add(connection)
        # Automatically add locations based on the connected room's name
        location_name = f'{connection.name}_entrance'
        self.travel_options.add(location_name)

    def add_character(self, character, location=None):
        if location is None:
            location = self.name  # By default, the character is in the main area of the room
        self.characters[character] = location

    def remove_character(self, character):
        self.characters.discard(character)

    def contains_character(self, character):
        return character in self.characters

    def start_room(self):
        if self.starting_character is not None:
            self.add_character(self.starting_character)

    def set_weapon(self, weapon):
        self.weapon = weapon

    def get_weapon(self):
        return self.weapon

    def get_state(self):
        return {
            'name': self.name,
            'characters': {char: loc for char, loc in self.characters.items()},
            'type': self.type,
            'travel_options': list(self.travel_options),
            'weapon': self.weapon,
        }
