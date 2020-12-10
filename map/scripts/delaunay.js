const fs = require('fs');
const path = require('path');
const Delaunator = require('delaunator');

module.exports = function(country, place) {
  const geojson = fs.readFileSync(path.resolve(__dirname, `../data/${country}_${place}_osm.geojson`));
  const geodata = JSON.parse(geojson);

  const points = [];
  for (let feature of geodata.features) {
    if (!feature) continue;
    points.push(feature.geometry.coordinates);
  }
  const delaunay = Delaunator.from(points);

  const lines = {
    type: 'FeatureCollection',
    features: []
  };
  const triangles = delaunay.triangles;
  for (let i = 0; i < triangles.length; i += 3) {
    for (let j = 0; j < 3; j++) {
      const origin = triangles[i+j];
      const destination = triangles[i+((j+1)%3)];
      lines.features.push({
        type: 'Feature',
        properties: {
          origin: origin,
          destination: destination
        },
        geometry: {
          type: 'LineString',
          coordinates: [
            points[origin],
            points[destination]
          ]
        }
      });
    }
  }

  const output = JSON.stringify(lines);
  fs.writeFileSync(path.resolve(__dirname, `../data/${country}_${place}_delaunay.geojson`), output, 'utf8');
  console.log('[delaunay] input:', geodata.features.length, ' delaunay:', lines.features.length);
}
