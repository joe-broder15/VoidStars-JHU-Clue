import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import axios from 'axios';
import Spinner from 'react-bootstrap/esm/Spinner';
import EndTurnButton from './EndTurnButton';

// this component will determine whether it is the viewing player's turn or not and display subcomponents accordingly
function Controls({ sessionId }) {
    const [gameState, setGameState] = useState({});
    const [loading, setLoading] = useState(true);
    const [isTurn, setIsTurn] = useState(false);
    const [checkTurn, setCheckTurn] = useState(true);

    // set an interval to get the state every second
    useEffect(() => {
        // get the state and re-render every second
        setTimeout(function () {
            if (checkTurn) {
                axios.post('http://127.0.0.1:5742/api/get_game_state',
                    {
                        "session_id": sessionId
                    })
                    .then(response => {
                        setGameState(response.data.state);
                        setLoading(false);
                        for (var i = 0; i < gameState.players.length; i++) {
                            if (gameState.players[i].session_id == sessionId && gameState.players[i].character == gameState.turn_character) {
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

                </Row>
                <Row>
                    <EndTurnButton sessionId={sessionId} setCheckTurn={()=>{setCheckTurn(true)}} setIsTurn={()=>{setIsTurn(false)}} setLoading={()=>{setLoading(true)}} setGameState={(t)=>{setGameState({})}}/>
                </Row>
            </Card.Body>
        </Card>
    );
};

export default Controls;
