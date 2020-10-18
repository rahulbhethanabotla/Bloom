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

    this.chart = React.createRef();
  }

  componentDidMount = async () => {
    const checkingsEndpoint = `${endpoints.queryEndpoint}accounts/checkings`;
    const response = await fetch(checkingsEndpoint, {
      headers: {
        phone: this.props.phone_number
      }
    });
    const user = await response.json();

    const collected_transactions = {};

    for (const {date, amount} of user.transactions) {
        const date_obj = new Date(date).toDateString();
        if (date_obj in collected_transactions) {
          collected_transactions[date_obj] += amount;
        } else {
          collected_transactions[date_obj] = amount;
        }
    }

    const sorted_transactions = Object.entries(collected_transactions).sort(([a,],[b,]) => new Date(a) - new Date(b));

    const sum_transactions = [];
    let sum = 0;

    for(const x of sorted_transactions){
        sum += x[1];
        sum_transactions.push(sum);
    }

    const dates = sorted_transactions.map(x => x[0]);
    const daily_transactions = sorted_transactions.map(x => x[1]);

    const daily_data = [];
    const sum_data = [];

    for(let i = 0; i < dates.length; i++) {
      daily_data.push({label: dates[i], y: daily_transactions[i]});
      sum_data.push({label: dates[i], y: sum_transactions[i]});
    }

    this.setState({
      daily_data,
      sum_data
    });
  };

  render() {
    const options = {
      theme: "light1",
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
          type: "stackedColumn",
          name: "Daily Transactions",
          color: "#e6739f",
          showInLegend: true,
        //   indexLabel: "{y[#index]}$",
          toolTipContent: "<strong>Date: {x}</strong></br> Transaction: {y}$",
          dataPoints: this.state.daily_data
        },
        {
          type: "stackedColumn",
          name: "Total Transactions",
          color: "#790c5a",
          showInLegend: true,
        //   indexLabel: "{y[#index]}$",
          toolTipContent: "<strong>Date: {x}</strong></br> Transaction: {y}$",
          dataPoints: this.state.sum_data
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
