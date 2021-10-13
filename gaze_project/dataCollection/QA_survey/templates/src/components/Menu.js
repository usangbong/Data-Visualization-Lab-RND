import React from 'react';
import MenuItem from 'components/MenuItem';


class Menu extends React.Component {

  onMenuClick = (page) => {
    this.props.onClick(page);
  }

  render() {
    const { page } = this.props;

    return (
      <ul className="menu-list">
        <li className="menu-item-wrapper">
          <MenuItem href="/data" title="Data" currentPage={page} onClick={this.onMenuClick}>+</MenuItem>
        </li>
        <li className="menu-item-wrapper">
          <MenuItem href="/analysis" title="Analysis view" currentPage={page} onClick={this.onMenuClick}>A</MenuItem>
        </li>
      </ul>
    );
  }
}

export default Menu;
