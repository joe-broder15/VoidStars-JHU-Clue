import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from 'axios';
import EventLog from './EventLog';
import Cards from './Cards';
import Spinner from 'react-bootstrap/esm/Spinner';

// component exists to hold control and display subcomponents
function Display({ sessionId }) {
    const [gameState, setGameState] = useState({});
    const [loading, setLoading] = useState(true);
    // set an interval to get the state every second
    useEffect(() => {
        // get the state and re-render every second
        setTimeout(function () {
            axios.post('http://127.0.0.1:5742/api/get_game_state',
                {
                    "session_id": sessionId
                })
                .then(response => {
                    // console.log(response.data.state);
                    setGameState(response.data.state);
                    setLoading(false);
                })
                .catch(error => {
                    console.error('Error creating post:', error);

                });
        }, 1000);
    });
    if (loading) {
        return(
            <Spinner/>
        );
    }

    return (
        <Card>
            <Card.Body>
                <Row>
                    <Col> 
                        board
                    </Col>
                    <Col> 
                        <EventLog events={gameState.events}/>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Cards sessionId={sessionId} players={gameState.players}/>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    );
};

export default Display;
