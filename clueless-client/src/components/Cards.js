import React, { useEffect, useState } from "react";
import ListGroup from "react-bootstrap/ListGroup";
import Badge from "react-bootstrap/Badge";

// this component displays a list of cards
function Cards({ sessionId, players }) {
  // state for cards
  const [cards, setCards] = useState([]);

  // iterates through the game state and grabs the list of cards
  useEffect(() => {
    // get the cards for the current player
    for (var i = 0; i < players.length; i++) {
      if (players[i].session_id == sessionId) {
        setCards(players[i].cards);
      }
    }
  });

  // render screen
  return (
    // render a listgroup and map cards to items
    <ListGroup as="ol" numbered>
      {cards.map((c) => (
        // each item to be rendered in the list
        <ListGroup.Item
          as="li"
          className="d-flex justify-content-between align-items-start"
        >
          <div className="ms-2 me-auto">
            <div className="fw-bold">{c.name}</div>
          </div>
          <Badge bg="primary" pill>
            {c.type}
          </Badge>
        </ListGroup.Item>
      ))}
    </ListGroup>
  );
}

export default Cards;
