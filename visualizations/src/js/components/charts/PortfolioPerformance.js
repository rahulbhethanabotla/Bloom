import React from "react";
import fetch from "node-fetch";

import endpoints from "endpoints.config";

import CanvasJSReact from "./canvasjs.react";
const CanvasJS = CanvasJSReact.CanvasJS;
const CanvasJSChart = CanvasJSReact.CanvasJSChart;
CanvasJS.addColorSet("niceColors", [
    // "#C8A1D6",
    // "#B096C8",
    // "#9A8CB9",
    // "#8481AA",
    // "#70769A",
    // "#5E6A8A",
    // "#4D5F7A",
    // "#3D546A",
    // "#2F485A",
    // "#233D4A",
    // "#18313B",
    // "#0F262D"
    "#003f5c",
    "#ffa600",
    "#bc5090",
    "#58508d",
    "#ff6361"
  ]);

export default class PortfolioPerformance extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dataPoints: []
    };

    this.chart = React.createRef();
  }

  addTicker = async ticker => {
    const stockEndpoint = `${endpoints.queryEndpoint}graphs/stock/performance`;
    const response = await fetch(stockEndpoint, {
        headers: {
            ticker
        }
    });
    const pData = await response.json();

    const performance = pData.performanceData;

    const dataPoints = []

    for(const x of performance) {
        dataPoints.push({x: new Date(x[0]), y: x[1]})
    }

    const graph = {
        type: "spline",
        name: ticker,
        xValueFormatString: "MMMM",
        showInLegend: true,
        toolTipContent:
        "<strong>Stock: {name}</strong> <br/> Change: {y}",
        dataPoints: dataPoints
    }

    const graphs = [...this.state.graphs];
    graphs.push(graph);

    this.setState({graphs});
  }

  componentDidMount = async () => {
    const portfolioPerformanceEndpoint = `${endpoints.queryEndpoint}graphs/portfolio/performance`;
    let response = await fetch(portfolioPerformanceEndpoint, {
        headers: {
            phone: this.props.phone_number
        }
    });
    const pData = await response.json();

    const performance = pData.performanceData;

    const dataPoints = []

    for(const x of performance) {
        dataPoints.push({x: new Date(x[0]), y: x[1]})
    }

    const portfolioEndpoint = `${endpoints.queryEndpoint}portfolio`;
    response = await fetch(portfolioEndpoint, {
        headers: {
            phone: this.props.phone_number
        }
    });
    const portfolioData = await response.json();
    const tickers = portfolioData.portfolio.map(x => x[0])

    for(const ticker of tickers) {
        this.addTicker(ticker);
    }

    this.setState({
      dataPoints,
      graphs: []
    });
  };

  render() {
    const graphs = this.state.graphs || [];
    const options = {
      theme: "light1",
      colorSet: "niceColors",
      exportEnabled: true,
      animationEnabled: true,
      title: {
        text: "Portfolio Performance",
        fontFamily: "geneva"
      },
      axisY: {
        title: "Change"
      },
      data: [
        {
          type: "spline",
          xValueFormatString: "MMMM",
          name: "Portfolio",
          showInLegend: true,
          toolTipContent:
          "<strong>Stock: {name}</strong> <br/> Change: {y}",
          dataPoints: this.state.dataPoints
        },
        ...graphs
      ]
    };
    return (
      <div>
        <CanvasJSChart options={options} ref={this.chart} />
      </div>
    );
  }
}
