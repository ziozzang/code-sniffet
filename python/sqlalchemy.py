from sqlalchemy import create_engine

# connection
conn = create_engine(
         conf['sql_connection'],
         #echo=True
       ).connect()

# disconnection
connection.close()
