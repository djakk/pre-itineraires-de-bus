import shapely
import shapely.geometry
# import shapely first, before geopandas_osm, to not crash when calling .unary_union()

import geopandas_osm
import geopandas_osm.osm

def get_data_from_osm():
  bbox = shapely.geometry.box(-1.6920,48.1506, -1.6753,48.1594)
  the_roads = geopandas_osm.osm.query_osm('way', bbox=bbox, recurse='down', tags='highway')
  the_roads = the_roads[the_roads.type == 'LineString'][['id', 'highway', 'name', 'geometry']].to_crs({'init': 'epsg:5837'}) # 5837 = 900913
  print(the_roads.unary_union) # à afficher dans qgis avec WKT
  return
