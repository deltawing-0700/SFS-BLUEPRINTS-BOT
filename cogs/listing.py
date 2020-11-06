from discord.ext import commands
import discord
from logics import organize
import glob, random
from main import client



class Listing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["List", "LIST"], brief = "Get all the blueprints page by page", description = "You can see all the blueprints this bot offers, page by page!")
    async def list(self, ctx, pgno=1):
        bplist=glob.glob("blueprints/*.bp")
        if pgno >= 1:
            result_list = organize(bplist, 30 , pgno-1)
            mess = "```"
            for i in result_list:
                mess += i + "\n"
            mess += "```"
            embed = discord.Embed(title="Blueprint Lookup", description=mess, color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Please use a value greater than or equal to zero")


    @commands.command(description="A better way to look at all blueprints this bot offers! (This command is a better version of the `list` command)")
    async def page(self, ctx):
        bplist=glob.glob("blueprints/*.bp")
        message = ""
        cur=0
        for i in organize(bplist, 30 , cur):
            #item = i.split("/")[1]
            message += f"{i} \n"
        embed = discord.Embed(
                    title = f"Page {cur + 1}/{(len(bplist) // 30) + 1}",
                    description=f"```{message}```")
        mess = await ctx.send(embed=embed)

        await mess.add_reaction("⬅️") 
        await mess.add_reaction("➡️")
        check = lambda reaction, user: client.user != user
        while True:
            res = await client.wait_for("reaction_add", check=check, timeout=60.0)
            if str(res[0]) == "➡️":
                try:
                    await mess.remove_reaction("➡️", ctx.author)
                except:
                    pass
                message = ""
                cur+=1
                try:
                    org_list = organize(bplist, 30 , cur)
                except:
                    await ctx.send(f"{ctx.author.mention} , There are no more pages")
                    break
                for i in org_list:
                    item = i.split("/")[1]
                    message += f"{item} \n"
                embed = discord.Embed(
                    title = f"Page {cur + 1}/{(len(bplist) // 30) + 1}",
                    description=f"```{message}```")
                await mess.edit(embed = embed)
            if str(res[0]) == "⬅️":
                if cur > 0:
                    try:
                        await mess.remove_reaction("⬅️", ctx.author)
                    except:
                        pass
                    message = ""
                    cur-=1
                    for i in organize(bplist, 30 , cur):
                        message += f"{i} \n"
                    embed = discord.Embed(
                        title = f"Page {cur + 1}/{(len(bplist) // 30) + 1}",
                        description=f"```{message}```")
                    await mess.edit(embed = embed)
                else:
                    await ctx.send(f"{ctx.author.mention} , You can No longer go backwards")
                    break


    @commands.command(aliases=["Search", "SEARCH"], description="Search for blueprints!")
    async def search(self, ctx, *, searchword: str):
        bplist=glob.glob("blueprints/*.bp")
        mess = "```"
        tmplst = []
        words = searchword.split()
        for word in words:
            for c in range(len(bplist)):
                if word.lower() in bplist[c].lower() and not bplist[c] in tmplst:
                    mess = mess + str(c) + ". " + bplist[c].split("/")[1] + "\n"
                    tmplst.append(bplist[c])
        if len(tmplst) == 0:
            mess = ""
            embed = discord.Embed(
                title=f"Search Results for {searchword}\n0 results found",
                description=mess,
                color=0xffa500)
        else:
            mess = mess + "```"
            embed = discord.Embed(
                title=
                f"Search Results for {searchword}\n{len(tmplst)} results found",
                description=mess,
                color=0xffa500)
        await ctx.send(embed=embed)

    @commands.command(aliases=["Count", "COUNT"], brief = "Know how many blueprint does the bot serve", description = "Get to know how many blueprints this bot offers till now!")
    async def count(self, ctx):
        bplist=glob.glob("blueprints/*.bp")
        total = len(bplist)
        embed = discord.Embed(
            description=f"Total Number of Blueprints Available - **{total}**",
            color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(aliases = ["Bp","BP"], description="Download Individual Blueprints with the Index Number.")
    async def bp(self, ctx,index:int):
        bplist=glob.glob("blueprints/*.bp")
        if index >=0:
            embed = discord.Embed(
            title="Blueprint",
            description="Here is your blueprint, if you have any problems, don't forget to report it to us! Contact Details can be found [here](https://sfsbp.xyz/contact.html)",
            color=0x00ff00)
            await ctx.send(embed=embed, file=discord.File(bplist[index]))

    @bp.error
    async def bp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("You need to enter your INDEX number! \nPlease check https://sfsbp.xyz/tutorials.html#tutorial2 for how to use the BP command \nor visit https://sfsbp.xyz/tutorials.html#tutorial3 for a guide on Index Numbers")
        if isinstance(error, commands.BadArgument):
            return await ctx.send("Numbers only accepted in index field, try again with a valid 'number'")
        await ctx.send(error)


    @commands.command(description="Don't want to choose? Take a randomly chosen BP!")
    async def randombp(self, ctx):
        bplist=glob.glob("blueprints/*.bp")
        randint = random.randint(0, len(bplist))
        await ctx.send(
            "Here is your blueprint", file=discord.File(bplist[randint]))

def setup(bot):
    bot.add_cog(Listing(bot))