import React from "react";
import FileAdd from "./ImageAdd";

import "./Modal.css";

export default class Modal extends React.Component {
  onClose = e => {
    this.props.onClose && this.props.onClose(e);
  };
  render() {
    if (!this.props.show) {
      return null;
    }
    return (
      <div class="modal" id="modal">
        <h2>Modal Window</h2>
        <div class="actions">
          <button class="toggle-button" onClick={this.onClose}>
            close
          </button>
        </div>
        <div class="sti_con">
            <h3>Stimulus</h3>
            <FileAdd></FileAdd>
        </div>
        <div class="data_con">
            <h3>Eye movement data</h3>
        </div>
        {/* <div class="content">{this.props.children}</div> */}
      </div>
    );
  }
}