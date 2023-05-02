import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import axios from "axios";
import Spinner from "react-bootstrap/esm/Spinner";
import EndTurnButton from "./EndTurnButton";
import Move from "./Move";
import Suggest from "./Suggest";
import Accuse from "./Accuse";
import Container from "react-bootstrap/esm/Container";

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

  const [suggestEnable, setSuggestEnable] = useState(false);

  const [winner, setWinner] = useState(null);

  // set an interval to get the state every second
  useEffect(() => {
    setTimeout(function () {
      // if we are checking for turns
      if (checkTurn) {
        // get the game state
        axios
          .post("http://127.0.0.1:5742/api/get_game_state", {
            session_id: sessionId,
          })
          .then((response) => {
            setGameState(response.data.state);
            setLoading(false);
            setWinner(gameState.winner);
            // check if it is currently our turn
            for (var i = 0; i < gameState.players.length; i++) {
              if (
                gameState.players[i].session_id == sessionId &&
                gameState.players[i].character == gameState.turn_character
              ) {
                // if so, stop checking for state and toggle that it is our turn
                console.log(gameState);
                setIsTurn(true);
                setCheckTurn(false);
                return;
              }
            }
          })
          .catch((error) => {
            console.error("Error creating post:", error);
          });
      }
    }, 1000);
  });

  // render based on state of the turn/game
  if (loading) {
    return <Spinner />;
  }
  if (winner != null) {
    return <h2>{winner} has won the game!</h2>;
  }
  if (!isTurn) {
    return <h2>it is not your turn yet</h2>;
  }
  return (
    <Container>
      <Row>
        {/* toggles between movement and suggestion */}
        {suggestEnable == true ? (
          <Col>
            <Suggest sessionId={sessionId} suggestEnable={suggestEnable} />
          </Col>
        ) : (
          <Col>
            <Move
              sessionId={sessionId}
              setSuggestEnable={() => {
                setSuggestEnable(true);
              }}
            />
          </Col>
        )}
        {/* accusation component */}
        <Col>
          <Accuse sessionId={sessionId} />
        </Col>
      </Row>
      <Row>
        {/* end turn button */}
        <EndTurnButton
          sessionId={sessionId}
          setCheckTurn={() => {
            setCheckTurn(true);
          }}
          setIsTurn={() => {
            setIsTurn(false);
          }}
          setLoading={() => {
            setLoading(true);
          }}
          setGameState={() => {
            setGameState({});
          }}
          setSuggestEnable={() => {
            setSuggestEnable(false);
          }}
        />
      </Row>
    </Container>
  );
}

export default Controls;
