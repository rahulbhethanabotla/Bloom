import React from "react";

import ChartHolder from "components/ChartHolder";
import CheckingsStats from "components/charts/CheckingsStats";
import PurchaseBreakdown from "components/charts/PurchaseBreakdown";
import PortfolioPerformance from "components/charts/PortfolioPerformance";

import "ContentHolder.sass";

export default class ContentHolder extends React.Component {

  constructor(props) {
    super(props);

    this.state = {phoneNumber: ""};
  }

  componentDidMount = () => {
    const phoneNumber = prompt("What's your phone number?");
    this.setState({phoneNumber});
  }

  render() {
    const phone_number = this.state.phoneNumber || "";
    return (
      <div id="contentHolder">
        <ChartHolder chart={<CheckingsStats phone_number={phone_number}/>} />
        <ChartHolder chart={<PurchaseBreakdown phone_number={phone_number}/>} />
        <ChartHolder chart={<PortfolioPerformance phone_number={phone_number}/>} />
      </div>
    );
  }
}
