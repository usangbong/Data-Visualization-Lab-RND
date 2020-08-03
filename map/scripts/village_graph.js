const fs = require('fs');
const path = require('path');

const delaunay = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_delaunay_cropped.json')));
const osm = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../data/kr_village_osm.json')));
const graph = [];

for (let feature of delaunay.features) {
  const prop  = feature.properties;

  if (!graph[prop.origin]) graph[prop.origin] = [];
  graph[prop.origin].push(prop.destination);
  graph[prop.origin].sort((a, b) => a - b);

  osm.features[prop.origin].properties.id = prop.origin;
  osm.features[prop.origin].properties.link = graph[prop.origin];
}

let output = JSON.stringify(graph);
fs.writeFile(path.resolve(__dirname, '../data/kr_village_delaunay_graph.json'), output, 'utf8', (err) => {
  if (err) throw err;
});
output = JSON.stringify(osm);
fs.writeFile(path.resolve(__dirname, '../data/kr_village_osm_linked.json'), output, 'utf8', (err) => {
  if (err) throw err;
});

console.log('input:', delaunay.features.length, ' delaunay_graph:', graph.length, ' osm_linked:', osm.features.length);
