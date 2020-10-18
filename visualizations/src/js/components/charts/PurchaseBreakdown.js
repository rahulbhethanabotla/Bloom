import React from "react";
import fetch from "node-fetch";

import endpoints from "endpoints.config";

import CanvasJSReact from "./canvasjs.react";
const CanvasJS = CanvasJSReact.CanvasJS;
const CanvasJSChart = CanvasJSReact.CanvasJSChart;

export default class PurchaseBreakdown extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dataPoints: []
    };

    this.chart = React.createRef();
  }

  normal = (mean, std) => {
    let s, u, v, norm;

    do {
      u = Math.random() * 2 - 1;
      v = Math.random() * 2 - 1;

      s = u * u + v * v;
    } while(s >= 1);

    norm = u * Math.sqrt(-2 * Math.log(s) / s);

    return std * norm + mean;
  }

  componentDidMount = async () => {
    const checkingsEndpoint = `${endpoints.queryEndpoint}accounts/metrics/purchases`;
    const response = await fetch(checkingsEndpoint, {
      headers: {
        phone: this.props.phone_number
      }
    });
    const breakdown = await response.json();

    const otherSize = 40;
    const std = 4;

    const largeUser = breakdown["largePurchasePercent"]["score"];
    const smallUser = breakdown["smallPurchasePercent"]["score"];
    const largeOther = breakdown["largePurchasePercent"]["classAverage"];
    const smallOther = breakdown["smallPurchasePercent"]["classAverage"];

    const other = [{label: "SMALL", y: smallOther, z: 80}, {label: "LARGE", y: largeOther, z: 80}];
    const you = [{label: "SMALL", y: smallUser, z: 70}, {label: "LARGE", y: largeUser, z: 70}];

    this.setState({
      other,
      you
    });
  };

  render() {
    const options = {
      theme: "light1",
      colorSet: "niceColors",
      exportEnabled: true,
      animationEnabled: true,
      title: {
        text: "Purchase Breakdown",
        fontFamily: "geneva"
      },
      axisX: {
        title: "Type of Purchase"
      },
      axisY: {
        title: "Percentage of Purchases",
        suffix: "%"
      },
      data: [
        {
          type: "bubble",
          name: "Others",
          showInLegend: true,
          color: "#432430",
        //   indexLabel: "{y[#index]}$",
          toolTipContent: "Percentage: {y}%",
          dataPoints: this.state.other
        },
        {
          type: "bubble",
          name: "You",
          showInLegend: true,
          color: "#F5847B",
        //   indexLabel: "{y[#index]}$",
          toolTipContent: "Percentage: {y}%",
          dataPoints: this.state.you
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
