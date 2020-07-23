import React, { Component } from 'react';

import SidebarMenu from './SidebarMenu';

const sideBar = {
  position: 'fixed',
  top: '20px',
  left: '0px',
  bottom: '20px',
};
const sidePanel = {
  float: 'left',
  height: '100%',
  backgroundColor: 'rgba(255, 255, 255, 1)',
  border: '2px solid black',
  overflow: 'hidden'
};
const buttonContainer = {
  float: 'left'
};
const sideFunctions = {
  width: '100%',
  height: '5%',
  backgroundColor: 'rgba(100, 100, 100, 1)'
};
const sideController = {
  width: '100%',
  height: '90%',
  backgroundColor: 'rgba(100, 100, 10, 1)'
};

export default class Sidebar extends Component {
  static defaultProps = {
    sideBarWidth: 300, // Sidebar width
    animationAmount: 10,
    animationInterval: 10
  };

  updatePanelWidth = () => {
    const { sideBarWidth, animationAmount, animationInterval } = this.props;
    let { width } = this.state;

    if (this.state.isOpened) {
      width += animationAmount;
      if (width > sideBarWidth) {
        width = sideBarWidth;
      } else {
        this.setState({ animation: setTimeout(this.updatePanelWidth, animationInterval) });
      }
    } else {
      width -= this.props.animationAmount;
      if (width < 0) {
        width = 0;
      } else {
        this.setState({ animation: setTimeout(this.updatePanelWidth, animationInterval) });
      }
    }
    this.setState({ width: width });
  }

  open = () => {
    this.setState({ isOpened: true });
    if (this.state.animation)
      clearTimeout(this.state.animation);
    this.setState({ animation: setTimeout(this.updatePanelWidth, this.props.animationInterval) });
  }

  close = () => {
    this.setState({ isOpened: false });
    if (this.state.animation)
      clearTimeout(this.state.animation);
    this.setState({ animation: setTimeout(this.updatePanelWidth, this.props.animationInterval) });
  }

  constructor(props) {
    super(props);
    this.state = {
      isOpened: true,
      width: props.sideBarWidth,
      animation: null
    };
  }

  render() {
    const { isOpened, width } = this.state;

    return (
      <div className="side-bar" style={sideBar}>
        <div className="side-panel" style={{width: `${width}px`, ...sidePanel}}>
          {/* Sidebar area */}
          <SidebarMenu></SidebarMenu>
        </div>
        <div className="button-container" style={buttonContainer}>
          {isOpened
            ? <button className="close" onClick={this.close}>&lt;</button>
            : <button className="open" onClick={this.open}>&gt;</button>
          }
        </div>
      </div>
    );
  }
}
