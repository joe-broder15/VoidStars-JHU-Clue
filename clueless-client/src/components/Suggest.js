import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Dropdown from 'react-bootstrap/Dropdown';

// this component will determine whether it is the viewing player's turn or not and display subcomponents accordingly
function Suggest({ sessionId, suggestDisabled, setMoveDisabled }) {
    const characters = ["Mrs. White", "Miss Scarlet", "Professor Plum", "Mr. Green", "Colonel Mustard", "Mrs. Peacock"];
    const [character, setCharacter] = useState("select a character");
    const weapons = ["Revolver", "Knife", "Lead Pipe", "Rope", "Candlestick", "Wrench"];
    const [weapon, setWeapon] = useState("select a weapon");
    const [canSuggest, setCanSuggest] = useState(false);
    const [location, setLocation] = useState("");

    // set an interval to get the state every second
    useEffect(() => {
        axios.post('http://127.0.0.1:5742/api/get_game_state',
            {
                "session_id": sessionId
            })
            .then(response => {
                // check if it is currently our turn
                var playerCharacter = "";
                var gameState = response.data.state;
                for (var i = 0; i < gameState.players.length; i++) {
                    // check if we can suggest
                    if (gameState.players[i].session_id == sessionId && gameState.players[i].character == gameState.turn_character) {
                        // if so, stop checking for state and toggle that it is our turn
                        setCanSuggest(gameState.players[i].can_suggest);
                        playerCharacter = gameState.players[i].character;
                    }
                }

                // get the room containing our character
                for (var i = 0; i < gameState.board.length; i++) {
                    // search through the room 
                    for (var j = 0; j < gameState.board[i].characters.length; j++) {
                        if (gameState.board[i].characters[j] == playerCharacter) {
                            setLocation(gameState.board[i].name);
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error creating post:', error);
            });
    }, []);

    function makeSuggestion() {
        if (character == "select a character" || weapon == "select a weapon") {
            return;
        }

        axios.post('http://127.0.0.1:5742/api/make_suggestion',
            {
                "session_id": sessionId,
                "character": character,
                "weapon": weapon,
                "location": location,
            })
            .then(response => {
                console.log(response.data);
                setCanSuggest(false);
                setMoveDisabled();
            })
            .catch(error => {
                console.error('Error creating post:', error);
            });
    }


    if (!canSuggest || suggestDisabled) {
        return (<h2>can't suggest</h2>);
    }
    return (
        <Card>
            <Card.Body>
                <Dropdown as={ButtonGroup}>
                    <Button variant="success">{character}</Button>

                    <Dropdown.Toggle split variant="success" id="dropdown-split-basic" />

                    <Dropdown.Menu>
                        {characters.map((c) => <Dropdown.Item value={c} onClick={e => setCharacter(c)}>{c}</Dropdown.Item>)}
                    </Dropdown.Menu>
                </Dropdown>
                <Dropdown as={ButtonGroup}>
                    <Button variant="success">{weapon}</Button>

                    <Dropdown.Toggle split variant="success" id="dropdown-split-basic" />

                    <Dropdown.Menu>
                        {weapons.map((w) => <Dropdown.Item value={w} onClick={e => setWeapon(w)}>{w}</Dropdown.Item>)}
                    </Dropdown.Menu>
                </Dropdown>
                <Button onClick={makeSuggestion}>Suggest</Button>
            </Card.Body>
        </Card>
    );
};

export default Suggest;
