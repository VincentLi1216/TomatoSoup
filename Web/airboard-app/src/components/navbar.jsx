import React, { Component } from "react";
import { Link } from "react-router-dom";

class NavBar extends Component {
  state = {};
  render() {
    return (
      <nav className="navbar navbar-light bg-light fixed-top p-0 shadow-sm">
        <Link
          to=""
          className="navStyle bg-light align-middle"
          style={{ textDecoration: "none" }}
        >
          <img
            src={require("../public/TomatoSoup.png")}
            className="iconImg"
            alt="TomatoSoupImg"
          />
          <strong>TomatoSoup</strong>
        </Link>
      </nav>
    );
  }
}

export default NavBar;
