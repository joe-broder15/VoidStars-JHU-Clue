import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Controls from "./Controls";
import Display from "./Display";

// component exists to hold control and display subcomponents
function GameView({ sessionId }) {
  return (
    <Card>
      <Card.Header>Clueless</Card.Header>
      <Card.Body>
        <Row>
          <Display sessionId={sessionId} />
        </Row>
        <Row>
          <Controls sessionId={sessionId} />
        </Row>
      </Card.Body>
    </Card>
  );
}

export default GameView;
