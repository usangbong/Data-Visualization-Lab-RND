# xeokit-bimserver-utils

A boilerplate utility that downloads IFC model metadata from BIMServer and writes it out as a JSON file that can be loaded into xeokit for offline BIM viewing.

Tested with [BIMServer V1.5.120](https://github.com/opensourceBIM/BIMserver/releases).

This utility downloads metadata for the latest revision of the given model.

The core utility script is in ````server.js````, which is executed by ````start.js````. This little bit of indirection helps us run this ES6 utility in node.js.

Configs for BIMServer authentication, the project ID, output file path etc. are constants within ````server.js```` - tweak those as required.

Find more info in the xeokit user guide: [Viewing BIM Models Offline](https://github.com/xeokit/xeokit-sdk/wiki/Viewing-BIM-Models-Offline).

## Building

This project requires [Node.js](https://nodejs.org/en/download/) to be installed.

````
git clone git@github.com:xeokit/xeokit-bimserver-utils.git
cd xeokit-bimserver-utils
npm install
npm run build
````

## Running

````
node start.js
````

The JSON metadata file will then be written within ````output```` (or wherever else you've configured ````server.js```` to write it).

