import geopandas


# line generalization : from one line to several points, by cutting lines in half
def generalize(the_geometries, the_generalization_size):
  
  the_geometries_generalized__as_a_list = []
  
  for a_geometry in the_geometries.itertuples():
    
    if a_geometry.geom_type != "LineString":
      continue
    
    the_length = a_geometry.geometry.length
    the_number_of_slices_to_be_done = 0
    while the_length >= the_generalization_size *0.5:
      the_length = the_length /2.0
      the_number_of_slices_to_be_done = 2* the_number_of_slices_to_be_done +1
    for a_slice in range(0, the_number_of_slices_to_be_done +1 +1):
      the_geometry_as_a_point = a_geometry.copy()
      the_fraction = a_slice / ( float(the_number_of_slices_to_be_done) +1 )
      the_geometry_as_a_point.geometry = a_geometry.geometry.interpolate(the_fraction, normalized=True)
      the_geometry_as_a_point['the_position'] = a_slice +1
      the_geometries_generalized__as_a_list.append(the_geometry_as_a_point)
  
  return geopandas.GeoDataFrame(the_geometries_generalized__as_a_list).reset_index(drop=True)
