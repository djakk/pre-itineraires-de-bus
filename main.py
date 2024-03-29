import sys
import os

import pika

import osm_io
import osm_io.from_osm
import osm_io.to_postgresql

import generalization
import generalization.line_generalization


print("Coucou ! (from print)")
sys.stdout.write("Coucou ! (from sys.stdout.write)")
sys.stdout.flush()


# Parse CLOUDAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url_str)


def aPrintingFunction(ch, method, properties, body):
    print("aPrintingFunction has been called !")
    print(properties)
    print(body)
    return

def theCallbackFunction(ch, method, properties, body):
    print("inside theCallbackFunction")
    
    the_datas = osm_io.from_osm.get_data_from_osm()
    print("after osm_io.from_osm.get_data_from_osm() : ")
    print(list(the_datas))
    print(the_datas)
    
    the_datas_2 = generalization.line_generalization.generalize(the_datas, 10)
    
    # geopandas -> postgresql database
    osm_io.to_postgresql.save_to_postgresql(the_datas_2, os.environ.get('DATABASE_URL'))
    
    # datas are ready inside the postgresql database : send a response back to NodeJS
    the_connection = pika.BlockingConnection(params)
    the_channel = the_connection.channel()
    the_channel.queue_declare(queue='myQueue3', durable=False)
    the_channel.basic_publish(exchange='', routing_key='myQueue3', body='the body')
    return


print("connection …")
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
print("channel …")
channel = connection.channel() # start a channel
#channel.queue_declare(queue='myQueue') # Declare a queue

print("channel.basic_consume …")
channel.basic_consume(theCallbackFunction,
    queue='myQueue2',
    no_ack=False) # no_ack=False <- if 'myQueue2' does not exists, do not sent a 404 error

print("channel.start_consuming …")
channel.start_consuming() # start consuming (blocks)

print("connection.close …")
connection.close()
