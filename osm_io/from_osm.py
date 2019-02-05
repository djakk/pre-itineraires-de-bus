import pandas

import shapely
import shapely.geometry
# import shapely first, before geopandas_osm, to not crash when calling .unary_union()

import geopandas_osm
import geopandas_osm.osm

def get_data_from_osm():
  """
  put the osm properties in a dict inside a row (instead of a column for each osm property)
  
  return a geodataframe with only 4 columns : id, osm_type ("way", "node" or "relation"), properties (dictionnary), geometry
  """
  bbox = shapely.geometry.box(-1.6920,48.1506, -1.6753,48.1594)
  #bbox = shapely.geometry.box(-1.6920,48.1506, -1.6910,48.1516) # very small bbox
  the_roads = geopandas_osm.osm.query_osm('way', bbox=bbox, recurse='down', tags='highway')
  #print("just after 'geopandas_osm.osm.query_osm' : ")
  #print(list(the_roads))
  #print(the_roads)
  
  # put the osm properties in a dict inside a row (instead of a column for each osm property)
  the_properties_as_name = list(the_roads)
  the_properties_as_name.remove('id')
  the_properties_as_name.remove('geometry')
  #print(the_properties_as_name)
  # this helped : pandas merge columns : https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python
  the_roads['properties'] = the_roads[the_properties_as_name].apply(lambda the_row: {a_property_as_name : the_row[a_property_as_name] for a_property_as_name in the_properties_as_name if pandas.notnull(the_row[a_property_as_name])}, axis=1)
  the_roads.drop(the_properties_as_name, axis=1, inplace=True)
  #print("just after '.apply' : ")
  #print(list(the_roads))
  #print(the_roads)
  
  the_roads = the_roads[the_roads.type == 'LineString'].to_crs({'init': 'epsg:5837'}) # 5837 = 900913
  
  # "osm_type" new column
  the_roads = the_roads.assign(osm_type = "way")
  
  #print(the_roads.unary_union) # à afficher dans qgis avec WKT
  return the_roads
