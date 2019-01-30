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
  
  var req = queryOverpass('[out:json];(rel(57.7,11.9,57.8,12.0)[route=tram][ref=3];rel(57.7,11.9,57.8,12.0)[route=tram][ref=10];);(._;>;);out;', function(err, geojson) {
    if (err) {
      res.end(err.message);
    } else {
      console.log("the overpass query has been done");
      console.log(geojson);
      
      var a_feature;
      for (a_feature in geojson.features) {
        console.log(a_feature.id);
        var the_colour_of_the_relation;
        try {
          console.log("where is the relation color ?");
          console.log(a_feature.properties);
          console.log(a_feature.properties.relations[0]);
          console.log(a_feature.properties.relations[0].reltags);
          the_colour_of_the_relation = a_feature.properties.relations[0].reltags.colour;
          console.log(the_colour_of_the_relation);
        } catch { };
        if (the_colour_of_the_relation) {
          a_feature.properties.tags["colour"] = the_colour_of_the_relation;
        }
      }
      
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
      s += '  <LineSymbolizer stroke="[colour]" />';
      s += ' </Rule>';
      s += '</Style>';
      s += '</Map>';
      
      // create map object
      var map = new mapnik.Map(1024, 1024);
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
      var the_image__for_the_map = new mapnik.Image(1024, 1024);
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
  }, { flatProperties: false });
}).listen(port);
