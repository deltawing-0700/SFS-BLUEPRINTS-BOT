from discord.ext import commands
import discord
from extensions import conn, get_cursor
from main import client
import random

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def changeprefix(self, ctx, prefix=None):
        if prefix == None:
            return await ctx.send("No prefix mentioned to be sent!")
        c = get_cursor()
        c.execute("SELECT * FROM prefixes WHERE serverid = %s", (ctx.guild.id, ))
        current = c.fetchone()
        if current is None:
            cursor = get_cursor()
            cursor.execute("INSERT INTO prefixes (serverid, prefix) VALUES (%s,%s)", (ctx.guild.id, prefix))
            conn.commit()
        else:
            cursor = get_cursor()
            cursor.execute("UPDATE prefixes set prefix = %s WHERE serverid = %s", (prefix, ctx.guild.id))
            conn.commit()
        await ctx.send(f"PREFIX SUCCESSFULLY UPDATED TO `{prefix}`")

    
    @changeprefix.error
    async def changeprefix_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only admins can run this command!")
        else:
            await ctx.send(error)


    @commands.Cog.listener()
    async def on_message(self, message):
        if client.user in message.mentions:
            c = get_cursor()
            c.execute("SELECT * FROM prefixes WHERE serverid=%s", (message.guild.id, ))
            pref = c.fetchone()
            if pref is None:
                return await message.channel.send(f"Heya, my prefix for `{message.guild}` is `$`")
            await message.channel.send(f"Heya, my prefix for `{message.guild}` is `{pref[1]}`")

def setup(bot):
    bot.add_cog(Prefix(bot))
            