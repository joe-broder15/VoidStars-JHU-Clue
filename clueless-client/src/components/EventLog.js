import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from 'axios';

// component exists to hold control and display subcomponents
function EventLog({events}) {
    // console.log(events[0]);
    return (
        <Card className='eventLogCard'>
            {events.map((e) => <p>{e.response}</p>)}
        </Card>
    );
};

export default EventLog;
