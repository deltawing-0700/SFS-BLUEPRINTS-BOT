from discord.ext import commands
import discord
from extensions import conn, get_cursor
from main import client
import random

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Shows this page.")
    async def help(self, ctx, command=None):
        c = get_cursor()
        c.execute('SELECT prefix FROM prefixes WHERE serverid=%s',(ctx.message.guild.id,))
        test = c.fetchone()
        if test == None:
            pfix = "$"
        else:
            pfix = test[0]
        colors = [discord.Colour.blue(), discord.Colour.blurple(), discord.Colour.dark_gold(), discord.Colour.dark_red(), discord.Colour.purple(), discord.Colour.green()]
        if command == None:
            embed = discord.Embed(
                title=f"{client.user.name} Help",
                description=f"Please use `{pfix}help <command>` for more details about a command.",
                color=random.choice(colors)
            )
            for cmd in client.commands:
                if cmd.brief == "verify":
                    pass
                else:
                    embed.add_field(name=f"{pfix}{cmd.name}", value=cmd.description or "No Description Available", inline=False)
            await ctx.send(embed=embed)
        else:
            for cmd in client.commands:
                if cmd.brief == "verify":
                    pass
                else:
                    d = client.get_command(command)
                    if d:
                        embed = discord.Embed(
                            title=f"{client.user.name} Help",
                            description=f"`{pfix}{d.name}`",
                            color=random.choice(colors)
                        )
                        embed.add_field(name="Description", value=d.description or "No Description Available")
                        embed.add_field(name="Usage", value=f"```{pfix}{d.name} {d.signature}```" or f"```{pfix}{d.name}```", inline=False)# no problem bro
                        h = ", ".join(d.aliases)
                        g = f"`{h}`"
                        if g == "``":
                            g = "No Aliases Available"
                        embed.add_field(name="Aliases", value=g or "No Aliases Available.", inline=False)
                        return await ctx.send(embed=embed)
                    else:
                        return await ctx.send("Command not found.")

    @commands.has_role("Blueprint Verifier")
    @commands.command(brief="verify")
    async def vhelp(self, ctx):
        c = get_cursor()
        c.execute('SELECT prefix FROM prefixes WHERE serverid=%s',(ctx.message.guild.id,))
        test = c.fetchone()
        if test == None:
            pfix = "$"
        else:
            pfix = test[0]
        embed = discord.Embed(
            title="Verifier Help",
            description="This section is only for verifiers! `T O P  S E C R E T`",
            color=discord.Colour.blue()
        )
        if ctx.guild.id == 689155797166325801:
            for cmd in client.commands:
                if cmd.brief == "verify":
                    if cmd.description == None:
                        cmd.description = "No Description."
                    else:
                        pass
                    embed.add_field(name=f"{pfix}{cmd.name}", value=f"Usage: `{pfix}{cmd.name} {cmd.signature}` \nDescription: {cmd.description}" or f"Usage: `{pfix}{cmd.name} {cmd.signature}`\nDescription: No Description.", inline=False)
                else:
                    pass
            await ctx.send(embed=embed)
        else:
            await ctx.send("This command is only for the SFS Blueprints Support server.")



def setup(bot):
    bot.add_cog(Help(bot))