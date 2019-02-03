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
  print(the_osm_datas.to_dict('records'))
  
  
  # work on the geometry column 
  the_osm_datas.geometry = the_osm_datas.geometry.wkb_hex()
  
  
  the_connection = psycopg2.connect(the_url_to_the_database)
  
  the_cursor = the_connection.cursor()
  the_cursor.execute("""DELETE FROM myTable;""")
  the_cursor.close()
  
  the_cursor = the_connection.cursor()
  the_cursor.executemany("""\
INSERT INTO myTable 
       (osm_id,   geometry) 
VALUES (%(id)s, ST_GeomFromText(%(geometry)s, 4326));\
""", the_osm_datas.to_dict('records'))
  the_cursor.close()
  
  the_connection.commit()
  the_connection.close()
  return
