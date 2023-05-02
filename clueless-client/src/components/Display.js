import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import axios from "axios";
import EventLog from "./EventLog";
import Cards from "./Cards";
import Spinner from "react-bootstrap/esm/Spinner";
import Board from "./Board";
import Container from "react-bootstrap/esm/Container";

// component exists to hold display subcomponents
function Display({ sessionId }) {
  const [gameState, setGameState] = useState({});
  const [loading, setLoading] = useState(true);
  // set an interval to get the state every second
  useEffect(() => {
    // get the state and re-render every second
    setTimeout(function () {
      axios
        .post("http://127.0.0.1:5742/api/get_game_state", {
          session_id: sessionId,
        })
        .then((response) => {
          setGameState(response.data.state);
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error creating post:", error);
        });
    }, 1000);
  });

  // render based on state
  if (loading) {
    return <Spinner />;
  }

  return (
    <Container>
      <Row>
        <Col>
          <Board board={gameState.board} />
        </Col>
      </Row>
      <br />
      <Row>
        <Col>
          <EventLog events={gameState.events} />
        </Col>
        <Col>
          <Cards sessionId={sessionId} players={gameState.players} />
        </Col>
      </Row>
    </Container>
  );
}

export default Display;
