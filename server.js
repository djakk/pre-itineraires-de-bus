var mapnik = require('mapnik');
var http = require('http');
var queryOverpass = require('query-overpass');

// register fonts and datasource plugins
mapnik.register_default_fonts();
mapnik.register_default_input_plugins();

// https://github.com/bensheldon/mapnik-on-heroku <- thanks !
var port = process.env.PORT || 3000;
var stylesheet = './stylesheet.xml';

http.createServer(function(req, res) {
  res.writeHead(500, {'Content-Type': 'text/plain'});
  
  var req = queryOverpass('[out:json];node(57.7,11.9,57.8,12.0)[amenity=bar];out;', function(err, geojson) {
    if (err) {
      res.end(err.message);
    } else {
      res.end(geojson);
    }
  });
  
  var map = new mapnik.Map(256, 256);
  map.load(stylesheet,
    function(err,map) {
      if (err) {
          res.end(err.message);
      }
      map.zoomAll();
      var im = new mapnik.Image(256, 256);
      map.render(im, function(err,im) {
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
  );
}).listen(port);
