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
  #the_roads = the_roads.groupby(by=the_properties_as_name, level=0, axis=1).apply(list)
  #the_roads = the_roads.groupby(by=["id", "geometry"], axis=1).apply(list)
  #the_roads = the_roads.groupby(by=["id", "geometry"], axis=1, level=0).groups
  # pandas merge columns : https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python
  #the_roads['properties'] = the_roads[the_properties_as_name].apply(lambda x: ''.join(x), axis=1)
  the_roads['properties'] = the_roads["name"] + the_roads["highway"]
  print("just after '.groupby' : ")
  print(list(the_roads))
  print(the_roads)
    
  the_roads = the_roads[the_roads.type == 'LineString'][['id', 'highway', 'name', 'geometry']].to_crs({'init': 'epsg:5837'}) # 5837 = 900913
  #print(the_roads.unary_union) # à afficher dans qgis avec WKT
  return the_roads
