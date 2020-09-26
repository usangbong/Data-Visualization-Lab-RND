import React from 'react';
import axios from 'axios';

class SpatialVariance extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      spRes: []
    };
  }

  componentDidMount() {
    axios.get(`http://${window.location.hostname}:5000/static/output/spatial_variance.json`)
      .then(response => {
        this.setState({
          spRes: 
            response.data
        });
      });
  }

  render() {
    const { spRes } = this.state;
    return (
      <>
        <div className="page-header">
          <h1>Spatial Variance</h1>
        </div>

    <p>{this.props.spRes}</p>

        <div className="page-section">
          <div style={{margin: '10px 0'}}>
            <button>A</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>B</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>C</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>D</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>E</button>
          </div>
        </div>
      </>
    );
  }
}

export default SpatialVariance;
