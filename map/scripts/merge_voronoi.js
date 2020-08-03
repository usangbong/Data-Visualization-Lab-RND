const fs = require('fs');
const path = require('path');
const turf = require('@turf/turf');

const geodata = [
  JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_voronoi_0-5000.json'))),
  JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_voronoi_4000-9000.json'))),
  JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_voronoi_10000-15000.json'))),
  JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_voronoi_15000-18782.json')))
];
const result = {
  type: 'FeatureCollection',
  features: []
};

for (let i = 0; i < geodata.length; i++) {
  const collection = geodata[i];
  let start = (i == 1) ? 1000 : 0;
  for (let j = start; j < collection.features.length; j++) {
    result.features.push(collection.features[j]);
  }
}

const output = JSON.stringify(result);
fs.writeFile(path.resolve(__dirname, `../data/kr_village_voronoi_merged.json`), output, 'utf8', (err) => {
  if (err) throw err;
  console.log(' output:', result.features.length);
});
