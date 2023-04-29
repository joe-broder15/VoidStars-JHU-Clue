import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from 'axios';
import Spinner from 'react-bootstrap/esm/Spinner';
import EndTurnButton from './EndTurnButton';
import Move from './Move';
import Suggest from './Suggest';

// this component will hold all of the controls and manage turns
function Controls({ sessionId }) {
    // game state
    const [gameState, setGameState] = useState({});
    // represents if the game is loading
    const [loading, setLoading] = useState(true);
    // represents if it is the player's turn
    const [isTurn, setIsTurn] = useState(false);
    // toggles checking for turns
    const [checkTurn, setCheckTurn] = useState(true);

    const [moveDisabled, setMoveDisabled] = useState(false);
    const [suggestReload, setSuggestReload] = useState(false);



    // set an interval to get the state every second
    useEffect(() => {
        setTimeout(function () {
            // if we are checking for turns
            if (checkTurn) {
                // get the game state
                axios.post('http://127.0.0.1:5742/api/get_game_state',
                    {
                        "session_id": sessionId
                    })
                    .then(response => {
                        setGameState(response.data.state);
                        setLoading(false);
                        // check if it is currently our turn
                        for (var i = 0; i < gameState.players.length; i++) {
                            if (gameState.players[i].session_id == sessionId && gameState.players[i].character == gameState.turn_character) {
                                // if so, stop checking for state and toggle that it is our turn
                                console.log(gameState);
                                setIsTurn(true);
                                setCheckTurn(false);
                                return;
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error creating post:', error);
                    });
            }

        }, 1000);
    });

    // render based on state of the turn/game
    if (loading) {
        return (
            <Spinner />
        );
    }
    if (!isTurn) {
        return (
            <h2>it is not your turn yet</h2>
        );
    }
    return (
        <Card>
            <Card.Body>
                <Row>
                    <Col><Move sessionId={sessionId} moveDisabled={moveDisabled} setSuggestReload={()=>{setSuggestReload(true)}} /></Col>
                    <Col><Suggest sessionId={sessionId} setMoveDisabled={()=>{setMoveDisabled(true)}} /></Col>
                    <Col>Accuse</Col>
                </Row>
                <Row>
                    <EndTurnButton sessionId={sessionId} setCheckTurn={() => { setCheckTurn(true) }} setIsTurn={() => { setIsTurn(false) }} setLoading={() => { setLoading(true) }} setGameState={(t) => { setGameState({}) }} />
                </Row>
            </Card.Body>
        </Card>
    );
};

export default Controls;
