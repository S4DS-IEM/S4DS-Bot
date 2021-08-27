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
    @tasks.loop(seconds = 30)
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


    # Error handling for 'meme' command
    @memes.error
    async def memes_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            e2 = discord.Embed(title = "Missing Required Arguement",  description = " Trigger the <memelist> command for getting correct index", color = discord.Color.blue())      
            e2.set_footer(text = "correct command: <prefix>memes <subreddit_index> <no.of_memes(limit=5)>")
            await ctx.send(embed = e2)
       

# Setup Cogs 'meme'
def setup(client):
    client.add_cog(meme(client))