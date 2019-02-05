import shapely
import shapely.geometry
# import shapely first, before geopandas_osm, to not crash when calling .unary_union()

import geopandas_osm
import geopandas_osm.osm

def get_data_from_osm():
  """
  put the osm properties in a dict inside a row (instead of a column for each osm property)
  """
  bbox = shapely.geometry.box(-1.6920,48.1506, -1.6753,48.1594)
  #bbox = shapely.geometry.box(-1.6920,48.1506, -1.6910,48.1516) # very small bbox
  the_roads = geopandas_osm.osm.query_osm('way', bbox=bbox, recurse='down', tags='highway')
  print("just after 'geopandas_osm.osm.query_osm' : ")
  print(list(the_roads))
  print(the_roads)
  
  # put the osm properties in a dict inside a row (instead of a column for each osm property)
  the_properties_as_name = list(the_roads)
  the_properties_as_name.remove('id')
  the_properties_as_name.remove('geometry')
  print(the_properties_as_name)
  the_roads = the_roads.groupby(by=the_properties_as_name, level=0, axis=1).first()
  print("just after '.groupby' : ")
  print(list(the_roads))
  print(the_roads)
    
  the_roads = the_roads[the_roads.type == 'LineString'][['id', 'highway', 'name', 'geometry']].to_crs({'init': 'epsg:5837'}) # 5837 = 900913
  #print(the_roads.unary_union) # à afficher dans qgis avec WKT
  return the_roads
