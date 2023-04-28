import React, { useEffect, useState } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import Badge from 'react-bootstrap/Badge';

// component exists to hold control and display subcomponents
function Cards({ sessionId, players }) {
    // state for cards
    const [cards, setCards] = useState([]);
    useEffect(() => {
        // get the cards for the current player
        for (var i = 0; i < players.length; i++) {
            if (players[i].session_id == sessionId) {
                setCards(players[i].cards);
            }
        }
    });
    return (
        // render a listgroup and map cards to items
        <ListGroup as="ol" numbered>
            {cards.map((c) =>
                <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
                    <div className="ms-2 me-auto">
                        <div className="fw-bold">{c.name}</div>
                    </div>
                    <Badge bg="primary" pill>
                        {c.type}
                    </Badge>
                </ListGroup.Item>
            )}
        </ListGroup>
    );
};

export default Cards;
