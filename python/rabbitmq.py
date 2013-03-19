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

