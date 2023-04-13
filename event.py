from enum import Enum

EventType = Enum("EventType", ["WIN", "LOSE", "MOVE", "ACCUSE", "SUGGEST", "START"])


class Event:
    event_count = 0

    def __init__(self, event_type, public_response, private_response, private_IDs):
        self.event_ID = Event.event_count
        self.event_type = event_type
        self.public_response = public_response
        self.private_response = private_response
        self.private_IDs = private_IDs
        Event.event_count += 1

    def get_state(self):
        return {
            "event_ID": self.event_ID,
            "event_type": self.event_type,
            "public_response": self.public_response,
            "private_response": self.private_response,
            "private_IDs": list(self.private_IDs),
        }
