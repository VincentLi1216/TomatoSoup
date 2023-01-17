import React, { Component } from "react";
import { Link } from "react-router-dom";

const month_olympic = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
const month_normal = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
const month_name = [
  "January",
  "Febrary",
  "March",
  "April",
  "May",
  "June",
  "July",
  "Auguest",
  "September",
  "October",
  "November",
  "December",
];

// Calendar component, with days component inside
class Calendar extends Component {
  state = {
    dayOfTheWeek: ["SUN", "MON", "TUE", "WEN", "THU", "FRI", "SAT"],
    day: this.props.day,
  };

  days_in_Month(month, year) {
    return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0
      ? month_olympic[month]
      : month_normal[month];
  }
  day_Start_intheMonth(month, year) {
    const tmpDate = new Date(year, month, 1);
    return tmpDate.getDay();
  }
  getButtonClasses(sday) {
    const { month, year, day, date } = this.props;
    if (
      (sday < day &&
        year === date.getFullYear() &&
        month === date.getMonth()) ||
      year < date.getFullYear() ||
      (year === date.getFullYear() && month < date.getMonth())
    ) {
      return "btn btn-light daysButton wordsFontColor";
    } else if (
      sday === day &&
      year === date.getFullYear() &&
      month === date.getMonth()
    ) {
      return "btn btn-light daysButton selectedFontColor";
    } else {
      return "daysButton disabledFontColor";
    }
  }

  render() {
    const { month, year } = this.props;
    const totalDay = this.days_in_Month(month, year);
    const firstDay = this.day_Start_intheMonth(month, year);
    console.log(this.state.day);
    // Days array
    const days = [];
    let n = -1;
    for (n; n >= -firstDay; n--) days.push(n);
    for (let i = 1; i <= totalDay; i++) days.push(i);
    const back = Math.ceil((totalDay + firstDay) / 7) * 7 - days.length;
    for (let i = 1; i <= back; i++) {
      days.push(n);
      n--;
    }

    return (
      <div className="calendar">
        {/* Title of the Calendar */}
        <h1 className="calMonth wordsFontColor">{month_name[month]}</h1>
        <h2 className="calYear wordsFontColor">{year}</h2>
        <button
          className="calMonthNext wordsFontColor fw-bold"
          onClick={this.props.onNextClicked}
        >
          <h1>▶</h1>
        </button>
        <button
          className="calMonthPrev wordsFontColor fw-bold"
          onClick={this.props.onPrevClicked}
        >
          <h1>◀</h1>
        </button>
        {/* Days of the week */}
        <ul className="daysOfTheWeek" key="dOTW">
          {this.state.dayOfTheWeek.map((day) => (
            <li key={day}>{day}</li>
          ))}
        </ul>
        {/* Days object */}
        <ul className="daysContainer" key="dE">
          {days.map((day) => (
            <li className="days" key={day}>
              {day > 0 &&
              this.getButtonClasses(day) !== "daysButton disabledFontColor" ? (
                // Days elements before && at today
                <Link
                  to={"gallery"}
                  onClick={() =>
                    this.props.onSelect(
                      (month + 1 < 10 ? "0" + (month + 1) : month + 1) +
                        "-" +
                        (day < 10 ? "0" + day : day) +
                        "-" +
                        year
                    )
                  }
                  style={{ textDecoration: "none" }}
                >
                  <button className={this.getButtonClasses(day)}>
                    <strong>{day}</strong>
                  </button>
                </Link>
              ) : day < 0 ? (
                // Empty days elements
                <div
                  className="daysButton wordsFontColor"
                  onClick={() => this.handleClick(day)}
                >
                  <strong>{null}</strong>
                </div>
              ) : (
                // Days elements after today
                <div className="daysAfter">
                  <button className={this.getButtonClasses(day)}>
                    <strong>{day}</strong>
                  </button>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default Calendar;
