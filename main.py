import sys
import os
import time

import pika


print("Coucou ! (from print)")
sys.stdout.write("Coucou ! (from sys.stdout.write)")
sys.stdout.flush()

time.sleep(30)

def aPrintingFunction(ch, method, properties, body):
    print(u"aPrintingFunction has been called !")
    return 0

# Parse CLOUDAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url)

print(u"connection …")
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
print(u"channel …")
channel = connection.channel() # start a channel
#channel.queue_declare(queue='myQueue') # Declare a queue

print(u"channel.basic_consume …")
channel.basic_consume(aPrintingFunction,
    queue='myQueue',
    no_ack=True)

print(u"channel.start_consuming …")
channel.start_consuming() # start consuming (blocks)

print(u"connection.close …")
connection.close()
