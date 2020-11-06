from discord.ext import commands
from extensions import get_cursor, conn
import discord
from main import client
import random

class Submission(commands.Cog):
    @commands.command(aliases=["submit", "Submit", "SUBMIT", "Upload", "UPLOAD"], description="Submit blueprints to the bot")
    async def upload(self, ctx, *, name):
        cursor = get_cursor()
        while True:
            randid = random.randint(10000,99999)
            cursor.execute("SELECT * FROM submissions WHERE id = %s", (randid,))
            total = cursor.fetchall()
            if len(total) == 0:
                break
        embed = discord.Embed(
            title="Blueprint Uploaded",
            description=f"Your Blueprint named `{name}`, with the (submission) id `{randid}` has been uploaded for verification! The 'Blueprint Verifiers' will check your blueprint and the bot will DM you regarding your BP's status. If it's not able to DM you, we'll DM you direct. \nMinimum Waiting Time: 1-2 days.",
            color=discord.Colour.dark_green()
        )
        notify = discord.Embed(
            title="Blueprint Submission Recieved",
            color=discord.Colour.dark_grey()
        )
        notify.add_field(name="Submitter", value=f"{ctx.author} \n({ctx.author.id})", inline=False)
        notify.add_field(name="Blueprint Name", value=name, inline=False)
        filename = f"submissions/{name}.bp"
        notify.add_field(name="File Path (in server, needed for debugging)", value=filename, inline=False)
        notify.add_field(name="Submission ID", value=randid)
        bpfile = ctx.message.attachments[0] 
        await bpfile.save(fp=f"submissions/{name}.bp")
        with open(filename, "r") as f:
            filecontent = f.read()
        cursor.execute(f"INSERT INTO submissions(id, name, bp, uid) VALUES(%s, %s, %s, %s)", (randid, filename, filecontent, ctx.author.id))
        conn.commit()
        cursor.execute(f"INSERT INTO submitstatus (id) VALUES (%s)", (randid,))
        conn.commit()
        await ctx.send(embed=embed)
        await client.get_channel(749900532034043905).send(embed=notify)



    @commands.has_role("Blueprint Verifier")
    @commands.command(brief="verify")
    async def submissions(self, ctx, index=None):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM submissions;")
        submissions_list = cursor.fetchall()
        if submissions_list:
            embed = discord.Embed(title="Submissions", color=discord.Colour.dark_gold())
            for item in submissions_list:
                subname = client.get_user(item[3]).name
                embed.add_field(name = item[1].split("/")[1], value = f"SubmissionID: {item[0]}\n submitter uid: {item[3]} \n submitter name: {subname}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Submissions list empty!")

    @submissions.error
    async def submissions_error(self, ctx, error):
        await ctx.send(error)
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Sorry, this command is meant for Blueprint Verifiers.") 

    @commands.command(brief="verify")
    async def verify(self, ctx, id:int):
        cursor = get_cursor()
        cursor.execute(f"SELECT * FROM submissions WHERE id = %s", (id,))
        d = cursor.fetchone()
        if not d == None:
            filename = str(d[1])
            with open(filename, "w") as f:
                f.write(d[2])
            await ctx.send("Here is your file for testing.", file=discord.File(filename))
        else:
            await ctx.send(f"Submission {id} doesn't exist. Consider rechecking.")


    @commands.command(brief="verify")
    async def approve(self, ctx, id:int):
        cursor=get_cursor()
        cursor.execute("SELECT * FROM submissions WHERE id = %s",(id,))
        submission = cursor.fetchone()
        if submission is None:
            return await ctx.send(f"Blueprint not found. ID {id} doesn't exist. Please re-check the submissions.")
        fname = submission[1].split("/")[1].split(".")[0]
        with open(f"blueprints/{fname}.bp", "w+") as f:
            f.write(submission[2])
            print("done")

        cursor = get_cursor()
        cursor.execute("INSERT INTO blueprints (name, bp) VALUES (%s,%s)", (fname,submission[2]))
        conn.commit()
        cursor.execute("UPDATE submitstatus SET status = %s, message = %s", ("Approved", "successfully verified"))
        conn.commit()
        sent_message = await ctx.send("File successfully added to the bot")
        embed = discord.Embed(description=f"The blueprint has been successfully verified and the file has been uploaded to main folder (blueprints/{submission[1]}")
        await sent_message.edit(content = "", embed = embed)
        bpname = fname
        try:
            embed = discord.Embed(
                title="Blueprint Verification Notification",
                description=f"The blueprint **{bpname}** submitted by you has been verified and has been uploaded to our server! Check it by searching {submission[1]}.",
                color=discord.Colour.green()
            )
            await client.get_user(submission[3]).send(embed=embed)
        except:
            await ctx.send(f"Unable to notify {client.get_user(submission[3])}. Manual interaction might be needed.")
        cursor.execute("DELETE FROM submissions WHERE ID = %s", (id,))
        conn.commit()


    @commands.command(brief="verify")
    async def deny(self, ctx, id:int, *, reason=None):
        cursor = get_cursor()
        cursor.execute(f"SELECT * FROM submissions WHERE id = %s", (id, ))
        subm = cursor.fetchone()
        if subm == None:
            return await ctx.send(f"Blueprint not found. ID {id} doesn't exist, consider rechecking.")
        else:
            bpname = subm[1].split("/")[1]
            cursor = get_cursor()
            cursor.execute("DELETE FROM submissions WHERE id = %s", (id, ))
            conn.commit()
            cursor.execute("UPDATE submitstatus SET status = %s, message = %s WHERE id = %s", ("Declined", reason, id))
            conn.commit()
            msg = await ctx.send(f"File {bpname} has been denied and has been removed from the database. Trying to connect with the author.")
            embed = discord.Embed(
                title="Blueprint Verification Notification",
                description=f"The blueprint **{bpname}** submitted by you has unfortunately been declined. Reason: **__{reason}__**. If you think this was a mistake, please contact us [here](https://sfsbp.xyz/contact.html)",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            try:
                await client.get_user(int(subm[2])).send(embed=embed)
                await msg.edit(f"File {bpname} has been denied and has been removed from the database. Successfully sent the DM to the user.")
            except:
                await ctx.send(f"Unable to send DM to {client.get_user(int(subm[2]))}. Manual interaction might be needed.")

def setup(bot):
    bot.add_cog(Submission(bot))