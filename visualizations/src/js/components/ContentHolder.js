import React from "react";

import ChartHolder from "components/ChartHolder";
// import PriceRange from "components/charts/PriceRange";
// import HaggleAnalysis from "components/charts/HaggleAnalysis";
// import OrderChart from "components/charts/OrderChart";
import CheckingsStats from "./charts/CheckingsStats";

import "ContentHolder.sass";

export default class ContentHolder extends React.Component {
  render() {
    return (
      <div id="contentHolder">
        <ChartHolder chart={<CheckingsStats />} />
        {/* <ChartHolder chart={<PriceRange />} />
        <ChartHolder chart={<HaggleAnalysis />} /> */}
      </div>
    );
  }
}
