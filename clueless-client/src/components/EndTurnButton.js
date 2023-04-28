import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import axios from 'axios';

// component exists to hold control and display subcomponents
function EndTurnButton({ sessionId, setCheckTurn, setIsTurn }) {

    function end_game() {
        axios.post('http://127.0.0.1:5742/api/end_turn',
            {
                "session_id": sessionId
            })
            .then(response => {
                setTimeout(function () {return}, 1000);
                setCheckTurn(true);
                setIsTurn(false);
            })
            .catch(error => {
                console.error('Error creating post:', error);
            });
    }

    return (
        <Button onClick={end_game}>End Turn</Button>
    );
};

export default EndTurnButton;
