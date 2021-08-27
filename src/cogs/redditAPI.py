# Imports
import discord
from discord.ext import commands,tasks
import random
import asyncpraw
import time
from asyncpraw.reddit import Subreddit
import json

ap_channel_list = []

#  Create a class 'meme' which inherits from the 'commands.Cog' class
class meme(commands.Cog):

    def __init__(self, client):
        self.client = client

    # 'Cog.listener' event which triggers autoposting in servers where it is enabled
    @commands.Cog.listener()
    async def on_ready(self):
        with open ('./cogs/autoid.json', 'r') as f:
            ap_channels = json.load(f)
        for i in ap_channels:
            if (ap_channels[i] != "0"):
                ap_channel_list.append(int(ap_channels[i]))
        self.test.start()


    # Command for getting a meme
    @commands.command()
    async def memes(self, ctx, arg : int, x = 1):
        
        reddit = asyncpraw.Reddit(client_id = "Vng40QEkdlR_VuVphsbxxA", client_secret = "4evSCjg47N9CTtQqqyQUuA8X2I4qXQ", username = "ProfessionalFloor135",  password =  "Qwerty@18606", user_agent = 'EduMemebot')
        memes_list = []
        f = open('./cogs/subreddit.txt', 'r')
        memes_list = f.readlines()
        f.close()

        if (x <= 5):
            if (arg > 0) and (arg <= len(memes_list)):
                subred = str(memes_list[arg-1])
                subreddit = await reddit.subreddit(subred)
                all_meme = []
                    
                hot = subreddit.hot(limit = 500)
                async for submission in hot:
                    all_meme.append(submission)
                    
                for i in range(x):
                    random_sub = random.choice(all_meme)
                    name = random_sub.title
                    url = random_sub.url
                    author = random_sub.author
                    pst = "https://www.reddit.com" + random_sub.permalink
                    
                    em = discord.Embed(title = name , url = pst, description = f'Created by u\{author}', colour = discord.Color.purple())
                    em.set_author(name = f'r\ {subred}')
                    em.set_image(url = url)
                    em.set_footer(text = f'Ordered by {ctx.author}', icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = em)
                    
            else:
                em1 = discord.Embed(title="Incorrect Index", description = " Trigger the <memelist> command for getting correct index" , color = discord.Color.blue(), inline = False)
                await ctx.send(embed= em1)
                
        else:
            em2 = discord.Embed(title = "Range Exceeded", description = "We are bound to provide you maximum 5 memes at a time", color = discord.Color.green())
            await ctx.send(embed = em2)

    # Command for starting AutoPost
    @commands.command(aliases = ['apon'])
    async def autoposton(self, ctx, channel : commands.TextChannelConverter):
        with open ('./cogs/autoid.json', 'r') as f:
            ap_channels = json.load(f)

        ap_channels[str(ctx.guild.id)] = str(channel.id)

        with open ('./cogs/autoid.json', 'w') as f:
            json.dump(ap_channels, f, indent = 4)
        ap_channel_list.append(channel.id)

    # Command for ending AutoPost
    @commands.command(aliases = ['apoff'])
    async def autopostoff(self, ctx):
        with open ('./cogs/autoid.json', 'r' ) as f:
            ap_channels = json.load(f)
        del_channel = int(ap_channels[str(ctx.guild.id)])
        ap_channels[str(ctx.guild.id)] = "0"

        with open ('./cogs/autoid.json', 'w') as f:
            json.dump(ap_channels, f, indent = 4)
        ap_channel_list.remove(del_channel)


    # Loop for autoposting every 15 minutes
    @tasks.loop(minutes = 15)
    async def test(self):
        
        reddit = asyncpraw.Reddit(client_id = "Vng40QEkdlR_VuVphsbxxA", client_secret = "4evSCjg47N9CTtQqqyQUuA8X2I4qXQ", username = "ProfessionalFloor135",  password =  "Qwerty@18606", user_agent = 'EduMemebot')
        memes_list = []
        f = open('./cogs/subreddit.txt', 'r')
        memes_list = f.readlines()
        f.close()
        
        subzero = random.choice(memes_list)
        subreddit = await reddit.subreddit(subzero)
        all_meme = []
        hot = subreddit.hot(limit = 500)
        async for submission in hot:
            all_meme.append(submission)
        random_sub = random.choice(all_meme)
        name = random_sub.title
        url = random_sub.url
        author = random_sub.author
        pst = "https://www.reddit.com" + random_sub.permalink
                    
        em8 = discord.Embed(title = name, url = pst, description = f'Created by u\{author}', colour = discord.Color.purple())
        em8.set_author(name = f'r\ {subzero}')
        em8.set_image(url = url)
        for channel_id in ap_channel_list:
            channel = self.client.get_channel(channel_id)
            await channel.send(embed = em8)

    # Command for getting the Subreddit List
    @commands.command()
    async def sublist(self, ctx):
        f = open('./cogs/subreddit.txt', 'r')
        memes_list = f.readlines()
        f.close()
        s = []
        for x in range(1,(len(memes_list)+1)):
            m = str(x) + f'. r\{memes_list[x-1]}'
            s.append(m)
        meme_list = ''.join(s)
        ema = discord.Embed(title = "Subreddit List", description = f"{meme_list}" , color = discord.Color.green(), inline = False)
        await ctx.send(embed = ema)

    # Command for adding a subreddit in the list (admin only command)
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def addsub(self, ctx, s):
        with open('./cogs/subreddit.txt', 'a+') as f5:
            f5.seek(0)
            data = f5.read(10000)
            if len(data) > 0 :
                f5.write("\n")
            f5.write(s)
            f5.close()

        memes_list = []
        f = open('./cogs/subreddit.txt', 'r')
        memes_list = f.readlines()
        f.close()
        s = []
        for x in range(1, (len(memes_list)+1)):
            m = str(x) + f'.  r\{memes_list[x-1]}'
            s.append(m)
        meme_list = ''.join(s)
        em9 = discord.Embed(title = "Subreddit Added Successfully", color = discord.Color.blue(), inline = False)
        em9.add_field(name = "Updated Subreddit List:\n", value = f"{meme_list}" , inline = False)
        await ctx.send(embed = em9)


    # Command for deleting a subreddit in the list (admin only command)
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def delsub(self, ctx, m : int):
        memes_list = []
        with open('./cogs/subreddit.txt', 'r+') as fp:
            memes_list = fp.readlines()
            if (m>0) and (m<=len(memes_list)):
                fp.seek(0)
                fp.truncate()
                memes_list.pop(m-1)
                memes_list[-1] = memes_list[-1].strip()
                fp.writelines(memes_list)
                fp.close()

                with open('./cogs/subreddit.txt', 'r') as sp:
                    list1 = sp.readlines()
                    sp.close()
                    s = []
                    for x in range(1, (len(list1)+1)):
                        m = str(x) + f'.  r\{list1[x-1]}'
                        s.append(m)
                    meme_list = ''.join(s)
                    em3 = discord.Embed(title = "Subreddit Deleted Successfully", color = discord.Color.blue(), inline = False)
                    em3.add_field(name = "Updated Subreddit List:\n", value = f"{meme_list}" , inline = False)
                    await ctx.send(embed = em3)
            else:
                em1= discord.Embed(title="Incorrect Index", 
                description = f"We only have {len(memes_list)} subreddits enlisted in our Subreddit List. \nTrigger the <sublist> command for getting correct Subreddit list" , 
                color = discord.Color.blue(), inline=False)
                await ctx.send(embed= em1)

    # Error handling for 'meme' command
    @memes.error
    async def memes_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            e2 = discord.Embed(title = "Missing Required Arguement",  description = " Trigger the <memelist> command for getting correct index", color = discord.Color.blue())      
            e2.set_footer(text = "correct command: <prefix>memes <subreddit_index> <no.of_memes(limit=5)>")
            await ctx.send(embed = e2)

    # Error handling for 'addsub' command
    @addsub.error
    async def addsub_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            e7 = discord.Embed(title = "{}, you are not an Administrator".format(ctx.author) , color= discord.Color.magenta())
            await ctx.send(embed = e7)
        elif isinstance(error, commands.MissingRequiredArgument):
            e2 = discord.Embed(title = "Missing Required Argument",  color = discord.Color.magenta())
            e2.set_footer(text = "correct command: <prefix>addsub  <correct subreddit name>")
            await ctx.send(embed = e2)
        
    # Error handling for 'delsub' command
    @delsub.error
    async def delsub_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            e5 = discord.Embed(title = "{}, you are not an Administrator".format(ctx.author), color = discord.Color.magenta())
            await ctx.send(embed = e5)
        elif isinstance(error, commands.MissingRequiredArgument):
            e2 = discord.Embed(title = "Missing Required Arguments", color = discord.Color.magenta())
            e2.set_footer(text = "correct command: <prefix>delsub  <index value of subreddit>")
            await ctx.send(embed = e2)
        elif isinstance(error, commands.BadArgument):
            e7 = discord.Embed(title = "Required Correct Argument", color = discord.Color.magenta())
            e7.set_footer(text = "correct command: <prefix>delsub  <index value of subreddit>")
            await ctx.send(embed = e7)
       
# Setup Cogs 'meme'
def setup(client):
    client.add_cog(meme(client))