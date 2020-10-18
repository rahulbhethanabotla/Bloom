import React from "react";
import fetch from "node-fetch";

import endpoints from "endpoints.config";

import CanvasJSReact from "./canvasjs.react";
const CanvasJS = CanvasJSReact.CanvasJS;
const CanvasJSChart = CanvasJSReact.CanvasJSChart;

export default class CheckingsStats extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dataPoints: []
    };
    CanvasJS.addColorSet("niceColors", [
      "#C8A1D6",
      "#B096C8",
      "#9A8CB9",
      "#8481AA",
      "#70769A",
      "#5E6A8A",
      "#4D5F7A",
      "#3D546A",
      "#2F485A",
      "#233D4A",
      "#18313B",
      "#0F262D"
    ]);

    this.chart = React.createRef();
  }

  componentDidMount = async () => {
    const rangesEndpoint = `${endpoints.queryEndpoint}accounts/checkings`;
    const response = await fetch(rangesEndpoint);
    const user = await response.json();

    console.log("User: ", user);

    const dataPoints = [];

    for (const {date, amount} of user.transactions) {
        dataPoints.push({ x: new Date(date), y: amount });  
    }

    console.log(dataPoints);

    this.setState({
      dataPoints
    });
  };

  render() {
    const options = {
      theme: "light1",
      colorSet: "niceColors",
      exportEnabled: true,
      animationEnabled: true,
      title: {
        text: "Transaction Data",
        fontFamily: "geneva"
      },
      axisX: {
        title: "Date"
      },
      axisY: {
        title: "Amount ($)",
        suffix: "$"
      },
      data: [
        {
          type: "scatter",
          markerSize: "15",
        //   indexLabel: "{y[#index]}$",
          toolTipContent:
            "<strong>Date: {x}</strong></br> Transaction: {y}$",
          dataPoints: this.state.dataPoints
        }
      ]
    };
    return (
      <div>
        <CanvasJSChart options={options} ref={this.chart} />
      </div>
    );
  }
}
