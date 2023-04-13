from event import *


def test_event_id():
    def helper():
        local_event = Event(EventType.WIN, "public", "private", "some id")

    helper()
    e = Event(EventType.WIN, "public", "private", "some id")
    assert e.event_ID == 1
