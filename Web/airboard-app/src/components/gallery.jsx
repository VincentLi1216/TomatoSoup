import React, { Component } from "react";
import { Link } from "react-router-dom";

class Gallery extends Component {
  state = {
    paths: null,
  };

  // Get paths when gallery got mounted
  componentDidMount() {
    let paths = [];
    fetch(this.props.urls)
      .then((response) => {
        return response.text();
      })
      .then((html) => {
        console.log(html);
        // Creat a DOMParser object to parse the html-type text
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        // Select all the line that contains urls needed
        let dirs = doc.querySelectorAll("html body pre a");
        for (let dir of dirs) {
          let temp = String(dir).split("/");
          if (temp[3] !== "") paths.push(temp[3]);
        }
        this.setState({ paths });
      })
      .catch(function (err) {
        console.log("Failed to fetch page: ", err);
      });
  }

  render() {
    const { paths } = this.state;
    const { urls, clicked_date } = this.props;
    return paths !== null ? (
      <div className="galleryRender">
        <p className="date_display">Date : {clicked_date}</p>
        {/* Render pics */}
        {paths.map((path) => (
          <div>
            <img src={urls + path} alt="pics" className="pics" />
          </div>
        ))}
      </div>
    ) : (
      <div className="galleryRender">
        <div className="pageNotFound">
          <p className="h2T">Oops!!</p>
          <Link to={"../"}>
            <img
              src={require("../public/TomatoSoup.png")}
              alt=""
              style={{ width: "15vh" }}
            />
          </Link>
          <p className="h3T">There seems to be nothing here.</p>
          <p className="h3T">Please check out the correct date.</p>
        </div>
      </div>
    );
  }
}

export default Gallery;
