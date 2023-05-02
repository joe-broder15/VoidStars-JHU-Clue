import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import axios from "axios";
import Container from "react-bootstrap/esm/Container";

// component exists to hold control and display subcomponents
function EventLog({ events }) {
  return (
    <Card>
      <Card.Header>Events</Card.Header>
      <Card.Body>
        <Container className="eventLogCard">
          {events
            .slice(0)
            .reverse()
            .map((e) => (
              <Row>
                <Card>
                  <Card.Body>{e.response}</Card.Body>
                </Card>
              </Row>
            ))}
        </Container>
      </Card.Body>
    </Card>
  );
}

export default EventLog;
