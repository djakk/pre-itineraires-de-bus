var mapnik = require('/app/node_modules/mapnik');
var http = require('http');

// register fonts and datasource plugins
mapnik.register_default_fonts();
mapnik.register_default_input_plugins();

var map = new mapnik.Map(256, 256);
