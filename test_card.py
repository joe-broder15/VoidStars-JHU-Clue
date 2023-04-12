from card import Card


# test that the card's get state returns the correct thing
def test_card_state():
    c1 = Card("name", "type")
    assert c1.get_state()["name"] == "name"
    assert c1.get_state()["type"] == "type"


# test the contains method
def test_card_contains():
    c1 = Card("gun", "weapon")
    assert c1.contains_clue("gun", "knife", "candlestick")
    assert not c1.contains_clue("library", "office", "drawing room")
