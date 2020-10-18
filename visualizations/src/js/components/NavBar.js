import React from "react";

import "NavBar.sass";

import logo from "logo.png";

const NavBar = () => {
  return (
    <div id="navBar">
      <img src={logo} alt="LOGO" />
      <h2>Bloom</h2>
      <h2>Analytics</h2>
    </div>
  );
};

export default NavBar;
