import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import Room from "./Room";
import Table from "react-bootstrap/Table";

// component exists to hold control and display subcomponents
function Board({ board }) {
  // console.log(events[0]);
  return (
    <Card>
      <Card.Header>Board</Card.Header>
      <Card.Body>
        <Table className="boardCard" bordered>
          <tbody>
            <tr>
              <Room room={board[0]} />
              <Room room={board[1]} />
              <Room room={board[2]} />
              <Room room={board[3]} />
              <Room room={board[4]} />
            </tr>
            <tr>
              <Room room={board[5]} />
              <Room room={0} />
              <Room room={board[6]} />
              <Room room={0} />
              <Room room={board[7]} />
            </tr>
            <tr>
              <Room room={board[8]} />
              <Room room={board[9]} />
              <Room room={board[10]} />
              <Room room={board[11]} />
              <Room room={board[12]} />
            </tr>
            <tr>
              <Room room={board[13]} />
              <Room room={0} />
              <Room room={board[14]} />
              <Room room={0} />
              <Room room={board[15]} />
            </tr>
            <tr>
              <Room room={board[16]} />
              <Room room={board[17]} />
              <Room room={board[18]} />
              <Room room={board[19]} />
              <Room room={board[20]} />
            </tr>
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  );
}

export default Board;
