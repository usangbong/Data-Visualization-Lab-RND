import React, { Component } from 'react';
import DropZone from './dropzone/DropZone';

class ImageAdd extends Component {
render() {
    return (
      <div>
        <div className="content">
            <DropZone />
        </div>
      </div>
    )
  }
}
export default ImageAdd;