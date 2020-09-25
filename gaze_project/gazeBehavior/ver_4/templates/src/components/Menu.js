import React from 'react';
import MenuItem from 'components/MenuItem';

class Menu extends React.Component {
  render() {
    return (
      <ul className="menu-list">
        <li className="menu-item-wrapper">
          <MenuItem href="/data" title="Data">+</MenuItem>
        </li>
        <li className="menu-item-wrapper">
          <MenuItem href="/spatial-variance" title="Spatial Variance">S</MenuItem>
        </li>
        <li className="menu-item-wrapper">
          <MenuItem href="/analysis" title="Analysis view">A</MenuItem>
        </li>
        <li className="menu-item-wrapper">
          <MenuItem href="/visualization" title="Visualization view">V</MenuItem>
        </li>
      </ul>
    );
  }
}

export default Menu;
