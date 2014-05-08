# connecting
connection = pika.BlockingConnection(
     pika.ConnectionParameters(
        host=conf['rabbit_host'],
        port=int(conf['rabbit_port']),
        credentials=pika.credentials.PlainCredentials(
          conf['rabbit_userid'],
          conf['rabbit_password']
        )
      )
    )

# disconnecting
connection.close()


#============================
#!/usr/bin/env python
import pika
import pickle
import conf

QUEUE_NAME = conf.RABBITMQ_QUEUE_NAME

def send(params):
  """
  RabbitMQ에 딕셔너리등을 전달.
  """
  connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=conf.RABBITMQ_INFO["hostname"]
      )
    )
  channel = connection.channel()
  channel.queue_declare(queue=QUEUE_NAME)
  channel.basic_publish(
      exchange='', routing_key=QUEUE_NAME,
      body=pickle.dumps(params)
    )


#=================================

def callbacks(ch, method, properties, body):
  purge_complete()
  p = pickle.loads(body)
  if p["command"] in cmd_agent.rlist.keys():
    create_thread(
        cmd_agent.rlist[p["command"]], p
      )

def do_recv():
  connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=conf.RABBITMQ_INFO["hostname"]
      )
    )
  channel = connection.channel()
  channel.queue_declare(queue=QUEUE_NAME)

  channel.basic_consume(
      callbacks, queue=QUEUE_NAME, no_ack=True
    )

  channel.start_consuming()
