import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Form from "react-bootstrap/Form";
import axios from "axios";
import Spinner from "react-bootstrap/Spinner";

// component
function StartGame({ sessionId, setGameStarted }) {
  // set an interval to get the state every second and check if the game has started
  useEffect(() => {
    // repeats the following every second
    const timer = setInterval(() => {
      axios
        .post("http://127.0.0.1:5742/api/get_game_state", {
          session_id: sessionId,
        })
        .then((response) => {
          console.log(response.data.state);
          if (response.data.state.status == "GameStatus.START") {
            setGameStarted(true);
            return;
          }
        })
        .catch((error) => {
          console.error("Error creating post:", error);
        });
    }, 1000);
    // clearing interval
    return () => clearInterval(timer);
  });

  // function to start the game
  function startGame() {
    axios
      .post("http://127.0.0.1:5742/api/start_game", {
        session_id: sessionId,
      })
      .then((response) => {
        console.log(response.data.state.status);
      })
      .catch((error) => {
        console.error("Error creating post:", error);
      });
  }

  // if there is no session id get the user to provide a username
  return (
    <Card>
      <Card.Header>Start Game</Card.Header>
      <Card.Body>
        <Card.Title>
          <Spinner />
        </Card.Title>
        <Card.Text>Click below to start the game.</Card.Text>
      </Card.Body>
      <Card.Body>
        <Button onClick={startGame}>Play</Button>
      </Card.Body>
    </Card>
  );
}

export default StartGame;
