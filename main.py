import sys
import os

import pika

import from_osm


print("Coucou ! (from print)")
sys.stdout.write("Coucou ! (from sys.stdout.write)")
sys.stdout.flush()


def aPrintingFunction(ch, method, properties, body):
    print(u"aPrintingFunction has been called !")
    print(properties)
    print(body)
    return 0

# Parse CLOUDAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url_str)

print(u"connection …")
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
print(u"channel …")
channel = connection.channel() # start a channel
#channel.queue_declare(queue='myQueue') # Declare a queue

print(u"channel.basic_consume …")
channel.basic_consume(from_osm.get_data_from_osm,
    queue='myQueue2',
    no_ack=False) # no_ack=False <- if 'myQueue2' does not exists, do not sent a 404 error

print(u"channel.start_consuming …")
channel.start_consuming() # start consuming (blocks)

print(u"connection.close …")
connection.close()
