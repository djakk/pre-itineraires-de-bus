import shapely
import geopandas
import pandas


# line generalization : from one line to several points, by cutting lines in half
def generalize(the_geometries, the_generalization_size):
  
  the_geometries['geometry'] = the_geometries['geometry'].apply(from_one_line_to_several_points, args=(the_generalization_size,))
  # from list inside a row to several rows, in a pandas' way
  # help : https://mikulskibartosz.name/how-to-split-a-list-inside-a-dataframe-cell-into-rows-in-pandas-9849d8ff2401 : 
  the_geometries = the_geometries.geometry.apply(pandas.Series) \
    .merge(the_geometries, left_index = True, right_index = True) \
    .drop("geometry", axis = 1) \
    .melt(id_vars = ['id', 'osm_type', 'properties'], value_name = "geometry") \
    .drop("variable", axis = 1) \
    .dropna(subset=["geometry"])
  
  print("After linestring -> points : ")
  print(list(the_geometries)) # print columns' name
  print(the_geometries)
  
  # the point having the most neighbours -> will fuse with them
  
  
  return the_geometries

def from_one_line_to_several_points(the_geometry, the_generalization_size):
  """
  by cutting lines in half
  """
  if the_geometry.geom_type != "LineString":
      return the_geometry
  
  the_length = the_geometry.length
  the_number_of_slices_to_be_done = 0
  while the_length >= the_generalization_size *0.5:
    the_length = the_length /2.0
    the_number_of_slices_to_be_done = 2* the_number_of_slices_to_be_done +1
    
  the_points = []
  for a_slice in range(0, the_number_of_slices_to_be_done +1 +1):
    the_fraction = a_slice / ( float(the_number_of_slices_to_be_done) +1 )
    the_points.append(the_geometry.interpolate(the_fraction, normalized=True))
  
  return the_points
