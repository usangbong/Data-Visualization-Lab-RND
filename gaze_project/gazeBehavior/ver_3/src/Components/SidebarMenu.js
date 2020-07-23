import React, { Component } from 'react';
import ReactDOM from "react-dom";

import Tabs from './Tabs';
import TabLink from './TabLink';
import TabContent from './TabContent';
import Modal from './Modal';

//import './Modal.css';

const styles = {
  tabs: {
    width: '100%',
    display: 'inline-block',
    marginRight: '30px',
    verticalAlign: 'top',
  },
  links: {
    margin: 0,
    padding: 0,
  },
  tabLink: {
    width: '50%',
    height: '30px',
    lineHeight: '30px',
    padding: '0 15px',
    cursor: 'pointer',
    border: 'none',
    borderBottom: '2px solid transparent',
    display: 'inline-block',
  },
  activeLinkStyle: {
    borderBottom: '2px solid #333',
  },
  visibleTabStyle: {
    display: 'inline-block',
  },
  content: {
    padding: '0 15px',
  },
};

class SidebarMenu extends Component{
  state = { show: false };

  showModal = () => {
    this.setState({ show: !this.state.show });
  };

  onClose = e => {
    this.props.show = false;
  };

  render(){
    return(
      <div id="plain-react">
        <Tabs
          activeLinkStyle={styles.activeLinkStyle}
          visibleTabStyle={styles.visibleTabStyle}
          style={styles.tabs}
        >
          <div style={styles.links}>
            <TabLink to="tab1" default style={styles.tabLink}>
              Tab1
            </TabLink>
            <TabLink to="tab2" style={styles.tabLink}>
              Tab2
            </TabLink>
          </div>

          <div style={styles.content}>
            <TabContent for="tab1">
              <h2>Tab1 content</h2>
              <button
                class="toggle-button"
                id="centered-toggle-button"
                onClick={e => {
                  this.showModal(e);
                }}
              >
                {" "}
                show Modal{" "}
              </button>
              <Modal onClose={this.showModal} show={this.state.show}>
                Message in Modal
              </Modal>


            </TabContent>
            <TabContent for="tab2">
              <h2>Tab2 content</h2>
              <div>TAB2 TEST</div>
            </TabContent>
          </div>
        </Tabs>
      </div>
    );
  }
}

export default SidebarMenu;
