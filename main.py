import sys
import os

import pika
import urllib.parse

print("Coucou ! (from print)")
sys.stdout.write("Coucou ! (from sys.stdout.write)")
sys.stdout.flush()


def aPrintingFunction(ch, method, properties, body):
    print(u"aPrintingFunction has been called !")
    return 0

# Parse CLOUDAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urllib.parse.urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='myQueue') # Declare a queue

channel.basic_consume(aPrintingFunction,
    queue='myQueue',
    no_ack=False)

channel.start_consuming() # start consuming (blocks)

connection.close()
