import psycopg2

def save_to_postgresql(the_datas, the_url_to_the_database):
  the_connection = psycopg2.connect(the_url_to_the_database)
  the_connection.close()
  return
