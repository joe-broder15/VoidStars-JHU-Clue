import "./App.css";
import Container from "react-bootstrap/Container";
import { useState } from "react";
import JoinGame from "./components/JoinGame";
import StartGame from "./components/StartGame";
import GameView from "./components/GameView";

/*
The root of our application, it is where we log the user in and start the game

*/
function App() {
  const [sessionId, setSessionId] = useState("");
  const [gameStarted, setGameStarted] = useState(false);

  // resolve the state of the game
  var content;
  // load the component for joining  a game if there is no session id
  if (sessionId == "") {
    content = (
      <JoinGame
        setGlobalId={(i) => {
          setSessionId(i);
        }}
      />
    );
  } else if (!gameStarted) {
    // load the component for getting a character if there is a session id
    content = (
      <StartGame
        sessionId={sessionId}
        setGameStarted={(i) => {
          setGameStarted(i);
        }}
      />
    );
  } else {
    // load the game view if we are done logging in
    content = <GameView sessionId={sessionId} />;
  }

  // render screen
  return <Container>{content}</Container>;
}

export default App;
