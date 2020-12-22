import React, { useEffect, useState, useRef } from 'react';

const mapboxToken = 'pk.eyJ1Ijoic2J1bXNlbyIsImEiOiJjajE0cXp5ZXYwMGswMnJvNjF3ZWhtOXU1In0.3lbBNI2-kpnz17nR8bpB3A';

function HeatMap(props) {
  const { width, height, data } = props;
  const [map, setMap] = useState(null);
  const svgRef = useRef();
  const mapboxgl = window.mapboxgl;

  useEffect(() => {
    const geodata = [];
    for (let i = 0; i < 3; i++)
      geodata[i] = {
        type: 'FeatureCollection',
        features: []
      };

    for (let row of data) {
      geodata[parseInt(row.new_person_id, 10)].features.push({
        type: 'Feature',
        properties: { ...row },
        geometry: {
          type: 'Point',
          coordinates: [row.local_position_y, row.local_position_x]
        }
      });
    }
    
    const colors = [
      'rgba(55,97,16,0)',
      'rgb(55,97,16)',
      'rgba(31,62,93,0)',
      'rgb(31,62,93)',
      'rgba(68,49,66,0)',
      'rgb(68,49,66)'
    ]

    mapboxgl.accessToken = mapboxToken;
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/dark-v10',
      center: [127.07, 37.5503],
      zoom: 12
    });

    map.on('load', () => {
      
      for (let i = 0; i < 3; i++) {
        map.addSource(`heatmap-${i}`, {
          type: 'geojson',
          data: geodata[i]
        });

        map.addLayer({
          id: `heatmap-${i}`,
          type: 'heatmap',
          source: `heatmap-${i}`,
          paint: {
            // Increase the heatmap weight based on frequency and property magnitude
            'heatmap-weight': 0.5,
            // Increase the heatmap color weight weight by zoom level
            // heatmap-intensity is a multiplier on top of heatmap-weight
            'heatmap-intensity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0,
              1,
              15,
              1
            ],
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['heatmap-density'],
              0, colors[i*2],
              0.1, colors[i*2+1]
            ],
            // Transition from heatmap to circle layer by zoom level
            'heatmap-opacity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, .5,
              15, .7
            ]
          }
        }, 'waterway-label');
      }
    });

    setMap(map);
  }, []);

  return (
    <>
      {typeof data === 'object' && data.length > 0 &&
        <div id="map" style={{ width: 600, height: 500 }}>
        </div>
      }
    </>
  );
}

export default HeatMap;
