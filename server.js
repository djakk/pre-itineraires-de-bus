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
  
  var req = queryOverpass('[out:json];(node,way(57.7,11.9,57.8,12.0)[railway];);out;', function(err, geojson) {
    if (err) {
      res.end(err.message);
    } else {
      console.log("the overpass query has been done");
      console.log(geojson);
      
      // map with just a style
      // eventually the api will support adding styles in javascript (!)
      var s = '<Map srs="+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs">';
      s += '<Style name="points">';
      s += ' <Rule>';
      s += '  <PointSymbolizer />';
      s += ' </Rule>';
      s += '</Style>';
      s += '<Style name="lines">';
      s += ' <Rule>';
      s += '  <LineSymbolizer />';
      s += ' </Rule>';
      s += '</Style>';
      s += '</Map>';
      
      // create map object
      var map = new mapnik.Map(256, 256);
      map.fromStringSync(s);
      
      console.log("creating the map …");
      var options = {
        type: 'geojson',
        inline: JSON.stringify(geojson)
      };
      console.log(options);
      
      var the_points_datasource = new mapnik.Datasource(options);
      var the_points_layer = new mapnik.Layer('points\' layer', "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs");
      the_points_layer.datasource = the_points_datasource;
      the_points_layer.styles = ['lines', 'points'];
      map.add_layer(the_points_layer);
      
      console.log("creating the image …");
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
