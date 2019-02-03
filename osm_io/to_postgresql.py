import psycopg2

def save_to_postgresql(the_osm_datas, the_url_to_the_database):
  """
  psql $DATABASE_URL -> 
    CREATE EXTENSION postgis;
    CREATE EXTENSION hstore;
    
    CREATE TABLE myTable (osm_id  bigint, properties  hstore, geometry  geometry);
  """
  print("inside 'save_to_postgresql'")
  print(the_osm_datas)
  #print(the_osm_datas.to_dict('records'))  
  
  
  the_connection = psycopg2.connect(the_url_to_the_database)
  
  the_cursor = the_connection.cursor()
  the_cursor.execute("""DELETE FROM myTable;""")
  the_cursor.close()
  
  the_osm_datas_as_records = the_osm_datas.to_dict('records')
  for a_record in the_osm_datas_as_records:
    
    # extract the non-null properties of the record, except id and geometry
    the_record_as_a_copy = dict(a_record)
    del the_record_as_a_copy["id"]
    del the_record_as_a_copy["geometry"]
    the_record_as_a_copy = { a_key : a_value for a_key, a_value in the_record_as_a_copy.items() if a_value is not None}
    a_record["properties"] = the_record_as_a_copy
    
    # work on the geometry column
    a_record["geometry"] = a_record["geometry"].wkb_hex
    
    print(a_record)
    
    the_cursor = the_connection.cursor()
    the_cursor.executemany("""\
INSERT INTO myTable 
       (osm_id,   geometry,     properties) 
VALUES (%(id)s, %(geometry)s, %(properties)s::hstore);\
""", a_record)
    the_cursor.close()
  
  the_connection.commit()
  the_connection.close()
  return
