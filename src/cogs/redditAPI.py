# Imports
import discord
from discord.ext import commands,tasks
import random
import asyncpraw
import time
from asyncpraw.reddit import Subreddit
import json


#  Create a class 'meme' which inherits from the 'commands.Cog' class
class meme(commands.Cog):

    def __init__(self, client):
        self.client = client


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