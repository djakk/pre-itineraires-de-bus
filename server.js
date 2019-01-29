var mapnik = require('mapnik');
var http = require('http');
var queryOverpass = require('query-overpass');

// register fonts and datasource plugins
mapnik.register_default_fonts();
mapnik.register_default_input_plugins();

// parts of code from https://github.com/bensheldon/mapnik-on-heroku <- thanks !
var port = process.env.PORT || 3000;
var stylesheet = './stylesheet.xml';

http.createServer(function(req, res) {
  res.writeHead(500, {'Content-Type': 'text/plain'});
  
  var req = queryOverpass('[out:json];node(57.7,11.9,57.8,12.0)[amenity=bar];out;', function(err, geojson) {
    if (err) {
      res.end(err.message);
    } else {
      //console.log(geojson);
      var map = new mapnik.Map(256, 256, "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs");
      var options = {
        type: 'geojson',
        inline: JSON.stringify(geojson)
      };
      var datasource = new mapnik.Datasource(options);
      var layer = new mapnik.Layer('layer\'s name', "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs");
      
      layer.datasource = datasource;
      map.layers.add(layer);
      
      map.zoomAll();
      var the_image__for_the_map = new mapnik.Image(256, 256);
      map.render(the_image__for_the_map, function(err,im) {
        if (err) {
          res.end(err.message);
        } else {
          im.encode('png', function(err,buffer) {
            if (err) {
              res.end(err.message);
            } else {
              res.writeHead(200, {'Content-Type': 'image/png'});
              res.end(buffer);
            }
          });
        }
      });
    }
  });
}).listen(port);
