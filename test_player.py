from player import *
from card import *

# test set character
def test_player_set_character():
    p = Player("key", "username", "character")

    p.set_character("not key", "character1")
    assert p.character == "character"

    p.set_character("key", "new character")
    assert p.character == "new character"

# test set username
def test_player_set_username():
    p = Player("key", "username", "character")

    p.set_username("not key", "username1")
    assert p.name == "username"

    p.set_username("key", "new username")
    assert p.name == "new username"

# test get clue
def test_player_get_clue():
    p = Player("key", "username", "character")

    # create 100 cards
    for i in range(100):
        c = Card(str(i), str(i))
        p.cards.add(c)

    assert not p.get_clue("2", "3", "4") == None
    assert not p.get_clue("2", "8000", "9000") == None
    assert p.get_clue("-2", "-3", "-4") == None
