const fs = require('fs');
const path = require('path');
const turf = require('@turf/turf');

const lng = process.argv[2];
const lat = process.argv[3];
const point = turf.point([lng, lat]);

const voronoi = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_voronoi.json')));

let found = false;
for (let feature of voronoi.features) {
  if (turf.inside(point, feature)) {
    console.log(feature);
    found = true;
    break;
  }
}
if (!found) {
  console.log('node not found.');
}
