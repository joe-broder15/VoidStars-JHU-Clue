import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import axios from "axios";
import Button from "react-bootstrap/esm/Button";
import ButtonGroup from "react-bootstrap/esm/ButtonGroup";

// this component will determine whether it is the viewing player's turn or not and display subcomponents accordingly
function Move({ sessionId, setSuggestEnable }) {
  const [hasMoved, setHasMoved] = useState(false);
  const [moves, setMoves] = useState([]);
  // set an interval to get the state every second
  useEffect(() => {
    axios
      .post("http://127.0.0.1:5742/api/get_available_moves", {
        session_id: sessionId,
      })
      .then((response) => {
        console.log(response.data);
        setMoves(response.data.availableMoves);
      })
      .catch((error) => {
        console.error("Error creating post:", error);
      });
  }, []);

  function makeMove(e) {
    axios
      .post("http://127.0.0.1:5742/api/move_player", {
        session_id: sessionId,
        location: e.target.value.replace(/ /g, "_").toUpperCase(),
      })
      .then((response) => {
        console.log(response.data);
        setHasMoved(true);
        setSuggestEnable();
      })
      .catch((error) => {
        console.error("Error creating post:", error);
      });
  }

  if (hasMoved) {
    return <h2>already moved</h2>;
  }
  return (
    <Card>
      <Card.Body>
        <ButtonGroup vertical>
          {moves.map((move) => (
            <Button value={move} onClick={(e) => makeMove(e)}>
              {move}
            </Button>
          ))}
        </ButtonGroup>
      </Card.Body>
    </Card>
  );
}

export default Move;
