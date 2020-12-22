const fs = require('fs');
const path = require('path');
const turf = require('@turf/turf');

module.exports = function(country, place) {
  // OSM 데이터 로드
  const osmJson = fs.readFileSync(path.resolve(__dirname, `../data/${country}_${place}_osm.geojson`));
  const osmData = JSON.parse(osmJson);

  // 보로노이 연산
  let voronoi = turf.voronoi(osmData, {});

  // 윤곽선 폴리곤 로드
  const boundJson = fs.readFileSync(path.resolve(__dirname, `../data/${country}_boundary.geojson`));
  const boundPolygon = JSON.parse(boundJson);
  const boundCoords = boundPolygon.features[0].geometry.coordinates;

  const result = {
    type: 'FeatureCollection',
    features: []
  };

  for (let i = 0; i < voronoi.features.length; i++) {
    if (!voronoi.features[i])
      continue;

    // 보로노이와 윤곽선 교차 연산
    //const voronoiIntersection = turf.intersect(voronoi.features[i], boundPolygon.features[0]);
    //console.log(voronoiIntersection);

    // properties 병합
    const feature = voronoi.features[i];
    feature.properties = {
      ...feature.properties,
      ...osmData.features[i].properties,
      osmcoord: osmData.features[i].geometry.coordinates
    };

    /*const multipolygon = [];
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
    }*/

    result.features.push(feature);
  }

  const output = JSON.stringify(result);
  fs.writeFileSync(path.resolve(__dirname, `../data/${country}_${place}_voronoi.geojson`), output, 'utf8');
  console.log('[voronoi] input:', osmData.features.length, ' voronoi:', voronoi.features.length, ' output:', result.features.length);
}
