import pika
import time
import os
import json

# Load module specs
f = open(os.path.dirname(__file__) + '/../module-name-specs.json')
specs = json.load(f)


# Set enviroment configs up. Default values can be changed by altering
# the second argument in each "get" call
FILES_SERVER = os.environ.get("FILES_SERVER", "localhost:3001")
QUEUE_SERVER_HOST, QUEUE_SERVER_PORT = os.environ.get(
    "QUEUE_SERVER", "localhost:5672").split(":")
Q_IN = os.environ.get("INPUT_QUEUE_NAME", specs["input_queue"])
Q_OUT = os.environ.get("OUTPUT_QUEUE_NAME", specs["output_queue"])
RECONNECT_TIMEOUT = os.environ.get("RECONNECT_TIMEOUT", 3)
RECONNECT_MAX = os.environ.get("RECONNECT_MAX", 30)


def getConnection():
    retries = 0
    try:
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                host=QUEUE_SERVER_HOST, port=QUEUE_SERVER_PORT, client_properties={"module_specs": specs})
        )
    except:
        retries += 1
        if (retries > RECONNECT_MAX):
            raise Exception("Failed to connect to server")
        print("Connection failed, attempt " + str(retries) +
              ". Retrying in " + str(RECONNECT_TIMEOUT) + " seconds...", flush=True)
        time.sleep(RECONNECT_TIMEOUT)
        return getConnection()


def callback(ch, method, properties, body):
    print("Running python test", flush=True)

    msg = json.loads(body)

    # The code bellow is the actual processing of the module. Here you can insert
    # whatever you want to do. The 'msg' dictonary contains all the input information
    # and the results should be inserted back in the same dictonary, that will be sent
    # to the output queue. As an example, currently all the input is given back as input
    # and the text is given back backwords.

    msg["echo-image"] = msg["input-image"]
    msg["echo-video"] = msg["input-video"]
    msg["backwords-text"] = msg["input-text"][::-1]

    # User code ends here.

    ch.basic_publish(exchange="", routing_key=Q_OUT, body=json.dumps(msg))

    print("Results sent.", flush=True)


def main():
    connection = getConnection()
    ch = connection.channel()
    ch.queue_declare(Q_IN, durable=True)
    ch.queue_declare(Q_OUT, durable=True)

    ch.basic_consume(queue=Q_IN, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages in " + Q_IN +
          ". Output will be sended to " + Q_OUT + ". To exit press CTRL+C", flush=True)
    ch.start_consuming()


main()
