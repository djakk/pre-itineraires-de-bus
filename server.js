var mapnik = require('mapnik');
var http = require('http');

var queryOverpass = require('query-overpass');

var ampqlib = require('amqplib');


// register fonts and datasource plugins
mapnik.register_default_fonts();
mapnik.register_default_input_plugins();

// parts of code from https://github.com/bensheldon/mapnik-on-heroku <- thanks !
var port = process.env.PORT || 3000;
var stylesheet = './stylesheet.xml';

http.createServer(function(req, res) {
  
  // trying to call python function aPrintingFunction through CloudAMPQ (queueing add-on)
  var q = 'myQueue2';
  var q3 = 'myQueue3';
  
  var url = process.env.CLOUDAMQP_URL || "amqp://localhost";
  console.log("ampqlib.connect …");
  var open = ampqlib.connect(url);
  
  // Consumer
  console.log("Consumer …");
  open.then(function(conn) {
    console.log("conn.createChannel …");
    var ok = conn.createChannel();
    ok = ok.then(function(ch) {
      console.log("ch.assertQueue …");
      ch.assertQueue(q3);
      console.log("ch.consume …");
      ch.consume(q3, function(msg) {
        console.log("inside ch.consume …");
        console.log(msg);
        if (msg !== null) {
          console.log(msg.content.toString());
          ch.ack(msg);
        }
      });
    });
    return ok;
  }).then(null, console.warn);
  
  // Publisher
  console.log("Publisher …");
  open.then(function(conn) {
    console.log("conn.createChannel …");
    var ok = conn.createChannel();
    ok = ok.then(function(ch) {
      console.log("assertQueue …");
      ch.assertQueue(q, {durable: false, noAck: true, the_argument: "blabla"});
      console.log("sendToQueue …");
      ch.sendToQueue(q, new Buffer('myBuffer2'));
    });
    return ok;
  }).then(null, console.warn);
  
  
  res.writeHead(500, {'Content-Type': 'text/plain'});
  
  var req = queryOverpass('[out:json];(rel(57.7,11.9,57.8,12.0)[route=tram][ref=3];rel(57.7,11.9,57.8,12.0)[route=tram][ref=10];);(._;>;);out;', function(err, geojson) {
    if (err) {
      res.end(err.message);
    } else {
      console.log("the overpass query has been done");
      console.log(geojson.features.length);
      
      for (var a_feature_index = 0; a_feature_index < geojson["features"].length; a_feature_index++) {
        var a_feature = geojson["features"][a_feature_index];
        var the_colour_of_the_relation;
        try {
          the_colour_of_the_relation = a_feature["properties"]["relations"][0]["reltags"]["colour"];
        } catch { };
        if (the_colour_of_the_relation) {
          //a_feature["properties"]["tags"]["colour"] = the_colour_of_the_relation;
          a_feature["properties"]["colour"] = the_colour_of_the_relation;
          //a_feature["colour"] = the_colour_of_the_relation;
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
