const { PythonShell } = require('python-shell');
const voronoi = require('./voronoi');
const delaunay = require('./delaunay');

const options = {
  scriptPath: 'scripts',
  args: ['-p', 'city', '-i', 2]
};
PythonShell.run('osm.py', options, (err, data) => {
  if (err) throw err;
  console.log(data[data.length-1]);
  voronoi(options.args[1]);
  delaunay(options.args[1]);
});
