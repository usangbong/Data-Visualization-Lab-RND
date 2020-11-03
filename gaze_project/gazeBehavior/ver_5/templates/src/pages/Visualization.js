import React from 'react';
import VisImage from 'components/VisImage';
import axios from 'axios';

class Visualization extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      stimulusPath: "",
      rawGazeData: []
    };
  }

  componentDidMount() {
    axios.get(`http://${window.location.hostname}:5000/static/output/stimulus_path.json`)
      .then(response => {
        this.setState({
          stimulusPath: 
            response.data
        });
      });
    axios.get(`http://${window.location.hostname}:5000/static/output/raw_gaze.json`)
      .then(response => {
        this.setState({
          rawGazeData: [
            response.data
          ]
        });
      });
  }

  render() {
    const { stimulusPath, rawGazeData } = this.state;
    return (
      <>
        <div className="page-header">
          <h1>Visualization</h1>
        </div>

        <div className="page-section">
          <div>
            <VisImage
              width="1024" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={[[700, 300], [700, 500], [1000, 300], [1000, 700], [1200, 900], [730, 800]]}
              circleSize="75"
            />
          </div>
          <div>
            <VisImage
              width="256" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={[[300, 300], [500, 300]]}
            />
            <VisImage
              width="256" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={[[300, 500], [700, 300]]}
            />
            <VisImage
              width="256" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={[[300, 500], [700, 300]]}
            />
            <VisImage
              width="256" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={[[300, 500], [700, 300]]}
            />
          </div>
        </div>
      </>
    );
  }
}

export default Visualization;
