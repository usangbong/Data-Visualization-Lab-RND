const fs = require('fs');
const path = require('path');

const delaunay = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_delaunay.json')));
const intersection = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_delaunay_intersection.json')));

const lines = {
  type: 'FeatureCollection',
  features: []
};
for (let i = 0; i < Math.min(delaunay.features.length, intersection.features.length); i++) {
  const delaunayCoord = delaunay.features[i].geometry.coordinates;
  const intersectionCoord = intersection.features[i].geometry.coordinates;

  if (intersectionCoord.length != 1)
    continue;
  else if (intersectionCoord[0].length != 2)
    continue;
  else if (!coordCompare(delaunayCoord, intersectionCoord[0])) {
    console.log(JSON.stringify(delaunayCoord), JSON.stringify(intersectionCoord[0]));
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
fs.writeFile(path.resolve(__dirname, '../data/kr_village_delaunay_cropped.json'), output, 'utf8', (err) => {
  if (err) throw err;
});

console.log('input(delaunay):', delaunay.features.length, ' input(intersection):', intersection.features.length, ' output:', lines.features.length);

function coordCompare(coord1, coord2) {
  const epsilon = 0.000001;
  for (let i = 0; i < 4; i++) {
    if (Math.abs(coord1[Math.floor(i/2)][i%2] - coord2[Math.floor(i/2)][i%2]) >= epsilon)
      return false;
  }
  return true;
}
