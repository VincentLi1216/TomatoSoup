import React, { Component } from "react";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import NavBar from "./navbar";
import Calendar from "./calendar";
import Gallery from "./gallery";

const date = new Date();
const year = date.getFullYear();
const month = date.getMonth();
const day = date.getDate();

class Airboard extends Component {
  state = {
    urls: null,
    selected_date: date,
    selected_year: year,
    selected_month: month,
    selected_day: day,
    clicked_date: null,
  };

  getURLs = (path) => {
    let temp = String(path).split("-");
    this.setState({
      urls: "http://122.116.234.117/images/" + path + "/",
      clicked_date: temp[0] + "/" + temp[1] + "/" + temp[2],
    });
  };
  prevMonth = () => {
    let { selected_month, selected_year } = this.state;
    selected_month--;
    if (selected_month < 0) {
      selected_year--;
      selected_month = 11;
    }
    this.setState({ selected_month, selected_year });
  };
  nexMonth = () => {
    let { selected_month, selected_year } = this.state;
    selected_month++;
    if (selected_month > 11) {
      selected_year++;
      selected_month = 0;
    }
    this.setState({ selected_month, selected_year });
  };

  render() {
    return (
      <BrowserRouter className="">
        <NavBar />
        <div className="content">
          <Routes>
            {/* Gallery */}
            <Route
              path="/gallery"
              element={
                <Gallery
                  urls={this.state.urls}
                  clicked_date={this.state.clicked_date}
                />
              }
            />
            {/* Calendar */}
            <Route
              path="/"
              element={
                <Calendar
                  onSelect={this.getURLs}
                  date={this.state.selected_date}
                  day={this.state.selected_day}
                  month={this.state.selected_month}
                  year={this.state.selected_year}
                  onNextClicked={this.nexMonth}
                  onPrevClicked={this.prevMonth}
                />
              }
            />
          </Routes>
        </div>
      </BrowserRouter>
    );
  }
}

export default Airboard;
