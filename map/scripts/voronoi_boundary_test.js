const fs = require('fs');
const path = require('path');
const turf = require('@turf/turf');

const geojson = fs.readFileSync(path.resolve(__dirname, '../data/kr_village_osm_test.json'));
const geodata = JSON.parse(geojson);
let voronoi = turf.voronoi(geodata, {});

const boundjson = fs.readFileSync(path.resolve(__dirname, '../data/kr_boundary.json'));
const bounddata = JSON.parse(boundjson);
const boundcoords = bounddata.features[0].geometry.coordinates;

const result = {
  type: 'FeatureCollection',
  features: []
};

let from = process.argv[2];
let to = process.argv[3];
if (from == undefined || from < 0)
  from = 0;
if (to == undefined || to > voronoi.features.length)
  to = voronoi.features.length;

for (let i = from; i < to; i++) {
  if (!voronoi.features[i])
    continue;

  console.log(`processing... (${i}/${to})`);

  const feature = voronoi.features[i];
  feature.properties = {
    ...feature.properties,
    ...geodata.features[i].properties
  };

  const multipolygon = [];
  for (let boundcoord of boundcoords) {
    const boundpolygon = turf.polygon(boundcoord);
    const intersection = turf.intersect(feature, boundpolygon);
    if (intersection != null && intersection.length > 0)
      multipolygon.push(intersection.geometry.coordinates);
  }
  console.log(multipolygon);

  if (multipolygon.length > 1) {
    feature.geometry = multipolygon;
  } else if (multipolygon.length == 1) {
    feature.geometry = multipolygon[0];
  }

  result.features.push(feature);
}

const output = JSON.stringify(result);
fs.writeFile(path.resolve(__dirname, `../data/kr_village_voronoi_test.json`), output, 'utf8', (err) => {
  if (err) throw err;
  console.log('input:', geodata.features.length, ' voronoi:', voronoi.features.length, ' output:', result.features.length);
});
