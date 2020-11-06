import discord
from discord.ext import commands
import sqlite3,time,os,glob
from os import getenv, remove
from mysql import connector
from logics import organize
from extensions import get_cursor, getprefix, conn
from dotenv import load_dotenv

load_dotenv()


print("starting bot!!")

        


client = commands.Bot(command_prefix=getprefix)

client.remove_command('help')
@client.event
async def on_ready():
    print("!!!!!")
    cursor = get_cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS blueprints (id INTEGER(50) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50), bp MEDIUMTEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY, name VARCHAR(50), bp MEDIUMTEXT, uid BIGINT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS prefixes (serverid INTEGER PRIMARY KEY, prefix VARCHAR(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS submitstatus (id INTEGER PRIMARY KEY, status VARCHAR(100) DEFAULT 'Pending', message VARCHAR(100))")
    print("Initiating downloads")

    cursor = get_cursor()
    cursor.execute("SELECT id,name,bp FROM blueprints;")
    results = cursor.fetchall()

    print("initiating writing")
    for result in results:
        with open(f"blueprints/{result[1]}.bp", "w") as f:
            f.write(result[2])
    print("bleprints downloaded")



"""@client.command()
async def add_cog(ctx, path):
    client.load_extension(path)
    await ctx.send("extension successfully loaded!")


@client.command()
async def remove_cog(ctx, path):
    client.unload_extension(path)
    await ctx.send("Extension removed successfully")


@add_cog.error
async def addcog_error(ctx, error):
    await ctx.send(f"error: {error}")"""


database = "database.db"
bplist = glob.glob("blueprints/*.bp")











client.load_extension("cogs.help")
client.load_extension("cogs.listing")
client.load_extension("cogs.submission")
client.load_extension("cogs.prefix")
client.load_extension("cogs.common")
#client.load_extension("cogs.topgg")


client.run(os.getenv("TOKEN"))
