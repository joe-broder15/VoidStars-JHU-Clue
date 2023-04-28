import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Form from 'react-bootstrap/Form';
import axios from "axios";

// component
function JoinGame({ setGlobalId }) {
    // initialize state
    const [sessionId, setSessionId] = useState("");
    const [username, setUsername] = useState("");
    const [character, setCharacter] = useState("");
    const [availableCharacters, setAvailableCharacters] = useState([]);

    // get a session id for a username and the list of available characters
    function joinGame() {
        axios.post('http://127.0.0.1:5742/api/join_game',
            {
                "username": username
            })
            .then(response => {

                setAvailableCharacters(response.data.available_characters);
                setSessionId(response.data.session_id);
                console.log(response.data);
            })
            .catch(error => {
                console.error('Error creating post:', error);
            });
    }

    // selects a character
    function selectCharacter(e) {
        axios.post('http://127.0.0.1:5742/api/set_character',
            {
                "character": e.target.value,
                "session_id": sessionId
            })
            .then(response => {
                console.log(response.data);
                setGlobalId(sessionId)
            })
            .catch(error => {
                console.error('Error creating post:', error);
            });
    }

    // if there is no session id get the user to provide a username
    if (sessionId == "") {
        return (
            <Card>
                <Card.Header>Join Game</Card.Header>
                <Card.Body>
                    <Card.Title>Welcome to Clueless</Card.Title>
                    <Card.Text>
                        Click below to join the game.
                    </Card.Text>
                    <Form>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                            <Form.Label>Username</Form.Label>
                            <Form.Control value={username} onChange={e => setUsername(e.target.value)} placeholder="please enter a username" />
                        </Form.Group>
                    </Form>
                </Card.Body>
                <Card.Body>
                    <Button onClick={joinGame}>Play</Button>
                </Card.Body>
            </Card>
        );


    } else { // otherwise pick a character
        return (
            <Card>
                <Card.Header>Select a character</Card.Header>
                <Card.Body>
                    <Card.Title>Welcome {username}</Card.Title>
                    <Card.Text>
                        please select a character
                    </Card.Text>
                </Card.Body>
                <Card.Body>
                    <ButtonGroup vertical>
                        {/* generate a list of buttons that allow you to set each character */}
                        {availableCharacters.map((character) => <Button value={character} onClick={e => selectCharacter(e)}>{character}</Button>)}
                    </ButtonGroup>
                </Card.Body>
            </Card>
        )
    }


};

export default JoinGame;
