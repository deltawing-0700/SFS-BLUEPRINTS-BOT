from discord.ext import commands
import time, discord
from main import client
import glob

class Common(commands.Cog):
    @commands.command(brief="see latency of the bot", description = "See how the bot performs, see ping,latency and response time")
    async def ping(self,ctx):
        start = time.perf_counter()
        embed = discord.Embed(description="**Websocket Latency** = Time it takes to recive data from the discord API\n**Response Time** = Time it takes between seeing your message then sending a response\n**Bot Latency** = Time needed to send/edit messages")
        embed.set_author(name='Ping')
        embed.set_footer(text=f"Asked by {ctx.author}")
        embed.add_field(name="Websocket Latency", value=f'{round(client.latency * 1000)}ms')
        message = await ctx.send(embed=embed)
        end = time.perf_counter()
        message_ping = (end - start) * 1000
        embed.set_author(name='Ping')
        embed.add_field(name="Response Time", value=f"{(message.created_at - ctx.message.created_at).total_seconds()/1000}ms")
        embed.add_field(name="Bot Latency", value=f"{round(message_ping)}ms")
        await message.edit(embed=embed)
        await ctx.send(f'My ping is {client.latency}!')


    @commands.command(aliases=["About", "ABOUT"], description="Get to know about the bot!")
    async def about(self,ctx):
        bplist=glob.glob("blueprints/*.bp")
        invite_url = "https://top.gg/bot/686127314353913856"
        embed = discord.Embed(
            title="SFS Blueprints",
            description=
            "SFS Blueprints can provide you with blueprints for SpaceFlight Simulator",
            color=0x00ff00,
            url=invite_url)
        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/avatars/686127314353913856/c36d272851ff1166c9da27a564f4de8f.png"
        )
        embed.add_field(name="Developer", value="DeltaWing \nWoozyDragon4018 \nSimple Astronaut", inline=False)
        embed.add_field(name="Language", value="Python (discord.Py)", inline=False)
        embed.add_field(
            name="Servers Joined", value=len(client.guilds), inline=False)
        embed.add_field(name="Release Date", value="12th of March, 2020", inline=False)
        embed.add_field(
            name="Number of Blueprints Available", value=len(bplist), inline=False)
        embed.add_field(name="Invite Link", value=invite_url, inline=False)
        embed.add_field(
            name="Support Server", value="https://discord.gg/3cxWFjd", inline=False)
        embed.add_field(name="Website", value="https://sfsbp.xyz", inline=False)
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Common(bot))