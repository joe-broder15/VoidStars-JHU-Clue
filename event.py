from enum import Enum

EventType = Enum(
    "EventType",
    [
        "WIN",
        "LOSE",
        "MOVE",
        "ACCUSE",
        "SUGGEST",
        "START",
        "PLAYER_ADDED",
        "SHOW",
        "TURN",
        "READY",
    ],
)


class Event:
    event_count = 0

    def __init__(self, event_type, public_response, private_response, private_ids=[]):
        self.event_ID = Event.event_count
        self.event_type = event_type
        self.public_response = public_response
        self.private_response = private_response
        self.private_IDs = private_ids
        Event.event_count += 1

    def get_state(self, session_id):
        resp = self.public_response
        if session_id in self.private_IDs:
            resp = self.private_response

        return {
            "event_ID": self.event_ID,
            "event_type": self.event_type,
            "response": resp,
        }
