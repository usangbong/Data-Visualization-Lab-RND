const fs = require('fs');
const path = require('path');

const datatable = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/uk_ltla_link_graph.json')));
const delaunay = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/uk_ltla_delaunay.geojson')));
const intersection = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/uk_ltla_delaunay_intersection.geojson')));

const lines = {
  type: 'FeatureCollection',
  features: []
};
for (let i = 0; i < delaunay.features.length; i++) {
  const origin = delaunay.features[i].properties.origin;
  const destination = delaunay.features[i].properties.destination;
  let intersectionIndex;

  try {
    intersectionIndex = datatable[origin].links[destination];
  } catch {
    continue;
  }
  if (intersectionIndex == undefined)
    continue;

  const delaunayCoord = delaunay.features[i].geometry.coordinates;
  const intersectionCoord = intersection.features[intersectionIndex].geometry.coordinates;

  if (intersectionCoord.length != 1)
    continue;
  else if (intersectionCoord[0].length != 2)
    continue;
  else if (!coordCompare(delaunayCoord, intersectionCoord[0])) {
    //console.log(JSON.stringify(delaunayCoord), JSON.stringify(intersectionCoord[0]));
    continue;
  }

  const feature = {
    type: 'Feature',
    properties: delaunay.features[i].properties,
    geometry: {
      type: 'LineString',
      coordinates: intersectionCoord[0]
    }
  };
  lines.features.push(feature);
}

const output = JSON.stringify(lines);
fs.writeFile(path.resolve(__dirname, '../data/uk_ltla_delaunay_cropped.geojson'), output, 'utf8', (err) => {
  if (err) throw err;
});

console.log('input(delaunay):', delaunay.features.length, ' input(intersection):', intersection.features.length, ' output:', lines.features.length);

function coordCompare(coord1, coord2) {
  const epsilon = 0.000001;
  let diff;

  for (let i = 0; i < 4; i++) {
    diff = Math.abs(coord1[Math.floor(i/2)][i%2] - coord2[Math.floor(i/2)][i%2]);
    if (diff >= epsilon)
      return false;
  }
  return true;
}
