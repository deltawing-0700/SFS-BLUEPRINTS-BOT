from mysql import connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE")
)
def get_cursor():
    global conn
    if conn.is_connected():
        return conn.cursor()
    else:
        conn = connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        print("database reconnected!")
        print(type(conn))
        return conn.cursor()

def getprefix(bot, message):
    id = message.guild.id
    c = get_cursor()
    c.execute('SELECT * FROM prefixes WHERE serverid = %s',(id,))
    user = c.fetchone()
    if str(user) == 'None':
        return "$"
    else:
        return user[1]