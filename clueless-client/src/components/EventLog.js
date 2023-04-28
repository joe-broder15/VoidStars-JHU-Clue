import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from 'axios';
import Container from 'react-bootstrap/esm/Container';

// component exists to hold control and display subcomponents
function EventLog({ events }) {
    // console.log(events[0]);
    return (
        <Container className='eventLogCard'>
            {/* <Card > */}
                {events.map((e) => <p>{e.response}</p>)}
            {/* </Card> */}
        </Container>

    );
};

export default EventLog;
