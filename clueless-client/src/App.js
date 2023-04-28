import './App.css';
import Container from 'react-bootstrap/Container'
import { useState } from 'react';
import JoinGame from './components/JoinGame';
import StartGame from './components/StartGame';
import GameView from './components/GameView';

/*
The root of our application, it is where we log the user in and start the game

*/
function App() {
    const [sessionId, setSessionId] = useState("");
    const [gameStarted, setGameStarted] = useState(false);

    // resolve the state of the game
    var content;
    if (sessionId == "") {
        content = <JoinGame setGlobalId={(i) => { setSessionId(i) }} />;
    } else if (!gameStarted) {
        content = <StartGame sessionId={sessionId} setGameStarted={(i) => { setGameStarted(i) }} />;
    } else {
        content = <GameView sessionId={sessionId}/>;
    }

    // render screen
    return (
        <Container>
            {content}
        </Container>
    );
}

export default App;
