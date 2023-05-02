import React, { useEffect, useState } from "react";
import Card from "react-bootstrap/Card";
import axios from "axios";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Dropdown from "react-bootstrap/Dropdown";

// this component will determine whether it is the viewing player's turn or not and display subcomponents accordingly
function Accuse({ sessionId }) {
  const characters = [
    "Mrs. White",
    "Miss Scarlet",
    "Professor Plum",
    "Mr. Green",
    "Colonel Mustard",
    "Mrs. Peacock",
  ];
  const [character, setCharacter] = useState("select a character");
  const weapons = [
    "Revolver",
    "Knife",
    "Lead Pipe",
    "Rope",
    "Candlestick",
    "Wrench",
  ];
  const [weapon, setWeapon] = useState("select a weapon");
  const locations = [
    "Study",
    "Hall",
    "Lounge",
    "Library",
    "Billiard Room",
    "Dining Room",
    "Conservatory",
    "Ballroom",
    "Kitchen",
  ];
  const [location, setLocation] = useState("select a location");

  const [hasAccused, setHasAccused] = useState(false);

  function makeAccusation() {
    if (
      character == "select a character" ||
      weapon == "select a weapon" ||
      location == "select a location"
    ) {
      return;
    }

    axios
      .post("http://127.0.0.1:5742/api/make_accusation", {
        session_id: sessionId,
        character: character,
        weapon: weapon,
        room: location,
      })
      .then((response) => {
        setHasAccused(true);
      })
      .catch((error) => {
        console.error("Error creating post:", error);
      });
  }

  if (hasAccused) {
    return <h2>Already Accused</h2>;
  }

  return (
    <Card>
      <Card.Header>Accuse</Card.Header>
      <Card.Body>
        {/* select a character */}
        <Dropdown as={ButtonGroup}>
          <Button variant="success">{character}</Button>

          <Dropdown.Toggle split variant="success" id="dropdown-split-basic" />

          <Dropdown.Menu>
            {characters.map((c) => (
              <Dropdown.Item value={c} onClick={(e) => setCharacter(c)}>
                {c}
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
        {/* select a weapon */}
        <Dropdown as={ButtonGroup}>
          <Button variant="success">{weapon}</Button>

          <Dropdown.Toggle split variant="success" id="dropdown-split-basic" />

          <Dropdown.Menu>
            {weapons.map((w) => (
              <Dropdown.Item value={w} onClick={(e) => setWeapon(w)}>
                {w}
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
        {/* select a location */}
        <Dropdown as={ButtonGroup}>
          <Button variant="success">{location}</Button>

          <Dropdown.Toggle split variant="success" id="dropdown-split-basic" />

          <Dropdown.Menu>
            {locations.map((l) => (
              <Dropdown.Item value={l} onClick={(e) => setLocation(l)}>
                {l}
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
        <Button onClick={makeAccusation}>Accuse</Button>
      </Card.Body>
    </Card>
  );
}

export default Accuse;
