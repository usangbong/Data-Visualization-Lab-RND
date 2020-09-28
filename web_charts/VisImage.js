import React from 'react';

class VisImage extends React.Component {
  constructor(props) {
    super(props);
    this.imageLayer = React.createRef();
    this.polygonLayer = React.createRef();
  }

  drawImage = url => {
    const { width, height, circles } = this.props;
    const canvas = this.imageLayer.current;
    const context = canvas.getContext('2d');
    const image = new Image();
    
    image.src = url;
    //console.log(url)
    image.onload = () => {
      const widthScale = width / image.width;
      const heightCalced = (height === 'auto') ? image.height * widthScale : height;
      const heightScale = heightCalced / image.height;
      const avgScale =  (widthScale + heightScale) / 2;

      this.imageLayer.current.height = heightCalced;
      this.polygonLayer.current.height = heightCalced;

      context.drawImage(image, 0, 0, width, heightCalced);
      if (typeof circles === 'object') {
        //console.log(circles);
        for (let position of circles) {
          this.drawCircle(position[0] * widthScale, position[1] * heightScale, 50 * avgScale, 5 * avgScale);
          //console.log(position)
        }
      }
    }
  }

  drawCircle = (x, y, radius, lineWidth) => {
    const canvas = this.polygonLayer.current;
    const context = canvas.getContext('2d');

    context.beginPath();
    context.arc(x, y, radius, 0, 2 * Math.PI);
    context.strokeStyle = '#ff0000';
    context.lineWidth = lineWidth;
    context.stroke();
  }

  componentDidMount() {
    const { image } = this.props;
    this.drawImage(image);
  }

  componentDidUpdate() {
    const { image } = this.props;
    this.drawImage(image);
  }

  render() {
    const { width, height } = this.props;

    return (
      <div className="vis-image">
        <canvas ref={this.imageLayer} className="vis-layer image-layer" width={width} height={height}></canvas>
        <canvas ref={this.polygonLayer} className="vis-layer polygon-layer" width={width} height={height}></canvas>
      </div>
    );
  }
}

export default VisImage;