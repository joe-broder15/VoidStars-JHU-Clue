import React, { useEffect, useState } from "react";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Table from "react-bootstrap/Table";

// component exists to hold control and display subcomponents
function Room({ room }) {
  if (room == 0) {
    return <Col sm={2}></Col>;
  }

  return (
    <td className="room" sm={2}>
      <b>{room.name}</b>
      <ul>
        {room.characters.map((c) => (
          <li>{c}</li>
        ))}
      </ul>
    </td>
  );
}

export default Room;
