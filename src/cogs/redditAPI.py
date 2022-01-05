# Imports
from os import name
import os
import discord
from discord.ext import commands,tasks
import random
import asyncpraw
import time
from asyncpraw.reddit import Subreddit
import json
from asyncpraw import Reddit

default_subreddits = ['DataScienceMemes\n', 'ProgrammerHumor\n', 'machinelearningmemes\n', 'mathmemes\n', 'linuxmemes\n', 'codingmemes\n', 'educationalmemes\n', 'applememes\n', 'windowsmemes']

subs_list = []

#  Create a class 'meme' which inherits from the 'commands.Cog' class
class meme(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ap_table_name = "public.autopostlist" # autopost table name

    # 'Cog.listener' event which triggers autoposting in servers where it is enabled
    @commands.Cog.listener()
    async def on_ready(self):

        # If doesn't exist, creates table pertaining to channels enabling autopost
        await self.client.pg_con.execute(f"CREATE TABLE IF NOT EXISTS {self.ap_table_name} (guild_id bigint NOT NULL, channel_id bigint NOT NULL, CONSTRAINT autopostlist_pkey PRIMARY KEY (guild_id), CONSTRAINT unique_channel UNIQUE (channel_id))")

        # If columns are deleted, to re-generate (with constraints)
        await self.client.pg_con.execute(f"ALTER TABLE IF EXISTS {self.ap_table_name} ADD COLUMN IF NOT EXISTS guild_id bigint NOT NULL CONSTRAINT autopostlist_pkey PRIMARY KEY")

        await self.client.pg_con.execute(f"ALTER TABLE IF EXISTS {self.ap_table_name} ADD COLUMN IF NOT EXISTS channel_id bigint NOT NULL CONSTRAINT unique_channel UNIQUE")

        self.autopost.start()

    # Activating meme services on joining a server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open ('./src/cogs/subred.json', 'r') as f:
            subs = json.load(f)
        
        if str(guild.id) not in subs:
            subs[str(guild.id)] = default_subreddits

            with open ('./src/cogs/subred.json', 'w') as f:
                json.dump(subs, f, indent = 4)
                subs_list.append(default_subreddits)
        
    # Deactivating meme services on leaving server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open ('./src/cogs/subred.json', 'r') as f:
            subs = json.load(f)
        subs.pop(str(guild.id))
        with open ('./src/cogs/subred.json', 'w') as f:
            json.dump(subs, f, indent = 4) 


    # Command for getting a meme
    memes_help ='''***Description :*** 
                            Command for getting a meme or a desired number of memes(not exceeding 5), based on user's wish\n
                            ***Syntax :***
                            `<prefix>memes <subreddit_index> <no.of_memes(limit=5)>`'''
    @commands.command(name ="memes", help = memes_help) 
    async def memes(self, ctx, arg : int, x = 1):

        guild = ctx.message.guild.id

        credentials = json.loads(os.environ['REDDIT_CREDENTIALS'])
        
        async with Reddit(**credentials) as reddit:
            with open ('./src/cogs/subred.json', 'r') as f:
                subs = json.load(f)
                memes_list = subs[str(guild)]

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
                        
                        embed = discord.Embed(title = name , url = pst, description = f'Created by u/{author}', colour = discord.Color.purple())
                        embed.set_author(name = f'r/{subred}')
                        embed.set_image(url = url)
                        embed.set_footer(text = f'Ordered by {ctx.author}', icon_url = ctx.author.avatar_url)
                        await ctx.send(embed = embed)
                        
                else:
                    embed_inc_index = discord.Embed(title="Incorrect Index", description = " Trigger the <memelist> command for getting correct index" , color = discord.Color.blue(), inline = False)
                    await ctx.send(embed= embed_inc_index)
                    
            else:
                embed_rng_exc = discord.Embed(title = "Range Exceeded", description = "We are bound to provide you maximum 5 memes at a time", color = discord.Color.green())
                await ctx.send(embed = embed_rng_exc)

    # Command for starting AutoPost
    autoposton_help = '''***Description :*** 
                            Command for starting AutoPost\n
                            ***Syntax :***
                            `<prefix>autoposton <channel_name>`''' 
    @commands.command(name ="autoposton", help = autoposton_help, aliases = ['apon'])
    async def autoposton(self, ctx, channel : commands.TextChannelConverter):
        await self.client.pg_con.execute(f"INSERT INTO {self.ap_table_name}(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, channel.id)

    # Command for ending AutoPost
    autopostoff_help = '''***Description :*** 
                            Command for ending AutoPost\n
                            ***Syntax :***
                            `<prefix>autopostoff`'''
    @commands.command(name ="autopostoff", help = autopostoff_help, aliases = ['apoff'])
    async def autopostoff(self, ctx):
        await self.client.pg_con.execute(f"DELETE FROM {self.ap_table_name} WHERE guild_id = $1", ctx.guild.id)

    # Loop for autoposting every 15 minutes
    @tasks.loop(seconds = 30)
    async def autopost(self):

        credentials = json.loads(os.environ['REDDIT_CREDENTIALS'])

        async with Reddit(**credentials) as reddit:

            subred_list = ['DataScienceMemes', 'ProgrammerHumor', 'machinelearningmemes', 'mathmemes', 'linuxmemes', 'codingmemes', 'educationalmemes', 'applememes', 'windowsmemes']
            
            random_sub = random.choice(subred_list)

            subreddit = await reddit.subreddit(random_sub)
            all_meme = []
            hot = subreddit.hot(limit = 500)
            async for submission in hot:
                all_meme.append(submission)
            random_sub = random.choice(all_meme)
            name = random_sub.title
            url = random_sub.url
            author = random_sub.author
            pst = "https://www.reddit.com" + random_sub.permalink

            ap_channel_data = await self.client.pg_con.fetch(f"SELECT * FROM {self.ap_table_name}")
                        
            embed = discord.Embed(title = name, url = pst, description = f'Created by u/{author}', colour = discord.Color.purple())
            embed.set_author(name = f'r/{random_sub}')
            embed.set_image(url = url)
            
            [await self.client.get_channel(channel_id).send(embed=embed) for guild_id, channel_id in ap_channel_data]

    # Command for getting the Subreddit List
    sublist_help = '''***Description :*** 
                            A list of available subreddit is displayed\n
                            ***Syntax :***
                            `<prefix>sublist` '''
    @commands.command(name ="sublist", help = sublist_help)
    async def sublist(self, ctx):
        
        guild = ctx.message.guild.id

        with open ('./src/cogs/subred.json', 'r') as f:
            subs = json.load(f)

        s = subs[str(guild)]
        n = []

        for x in range(1,(len(s)+1)):
            m = str(x) + f'. r/{s[x-1]}'
            n.append(m)
        meme_list = ''.join(n)
        embed = discord.Embed(title = "Subreddit List", description = f"{meme_list}" , color = discord.Color.green(), inline = False)
        await ctx.send(embed = embed)

    # Command for adding a subreddit in the list (admin only command)
    addsub_help = '''***Description :*** 
                            Adds a subreddit within the existing list\n
                            ***Syntax :***
                            `<prefix>addsub <subreddit_name>` \n
                            **Permissions Required :**
                            `Administrator`'''
    @commands.command(name ="addsub", help = addsub_help)
    @commands.has_permissions(administrator = True)
    async def addsub(self, ctx, s):

        subred_list = []
        guild = ctx.message.guild.id

        with open ('./src/cogs/subred.json', 'r') as f:
            subs = json.load(f)
        
        memes_list = subs[str(guild)]
        last_second_sub = memes_list[-1] + '\n'
        memes_list.pop()
        memes_list.append(last_second_sub)
        memes_list.append(str(s))

        with open ('./src/cogs/subred.json', 'w') as f:
            json.dump(subs, f, indent = 4)
            subred_list.append(memes_list)

        s = []
        for x in range(1, (len(memes_list)+1)):
            m = str(x) + f'.  r/{memes_list[x-1]}'
            s.append(m)
        meme_list = ''.join(s)
        embed = discord.Embed(title = "Subreddit Added Successfully", color = discord.Color.blue(), inline = False)
        embed.add_field(name = "Updated Subreddit List:\n", value = f"{meme_list}" , inline = False)
        await ctx.send(embed = embed)


    # Command for deleting a subreddit in the list (admin only command)
    delsub_help = '''***Description :*** 
                            Deletes a subreddit from a given index\n
                            ***Syntax :***
                            `<prefix>delsub <index>` \n
                            **Permissions Required :**
                            `Administrator`'''
    @commands.command(name ="delsub",  help = delsub_help)
    @commands.has_permissions(administrator = True)
    async def delsub(self, ctx, m : int):
        
        subred_list = []
        guild = ctx.message.guild.id

        with open ('./src/cogs/subred.json', 'r') as f:
            subs = json.load(f)
            memes_list = subs[str(guild)]
            if (m>0) and (m<=len(memes_list)):
                memes_list.pop(m-1)
                memes_list[-1] = memes_list[-1].strip()

                with open ('./src/cogs/subred.json', 'w') as f:
                    json.dump(subs, f, indent = 4)
                    subred_list.append(memes_list)

                    s = []
                    for x in range(1, (len(memes_list)+1)):
                        m = str(x) + f'.  r/{memes_list[x-1]}'
                        s.append(m)
                    meme_list = ''.join(s)
                    embed = discord.Embed(title = "Subreddit Deleted Successfully", color = discord.Color.blue(), inline = False)
                    embed.add_field(name = "Updated Subreddit List:\n", value = f"{meme_list}" , inline = False)
                    await ctx.send(embed = embed)
            else:
                embed_inc_index= discord.Embed(title="Incorrect Index", 
                description = f"We only have {len(memes_list)} subreddits enlisted in our Subreddit List. \nTrigger the <sublist> command for getting correct Subreddit list" , 
                color = discord.Color.blue(), inline=False)
                await ctx.send(embed= embed_inc_index)

    # Error handling for 'meme' command
    @memes.error
    async def memes_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = "Missing Required Arguement",  description = " Trigger the <memelist> command for getting correct index", color = discord.Color.blue())      
            embed.set_footer(text = "correct command: <prefix>memes <subreddit_index> <no.of_memes(limit=5)>")
            await ctx.send(embed = embed)

    # Error handling for 'addsub' command
    @addsub.error
    async def addsub_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed_not_admin = discord.Embed(title = "{}, you are not an Administrator".format(ctx.author) , color= discord.Color.magenta())
            await ctx.send(embed = embed_not_admin)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed_miss_req_arg = discord.Embed(title = "Missing Required Argument",  color = discord.Color.magenta())
            embed_miss_req_arg.set_footer(text = "correct command: <prefix>addsub  <correct subreddit name>")
            await ctx.send(embed = embed_miss_req_arg)
        
    # Error handling for 'delsub' command
    @delsub.error
    async def delsub_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed_not_admin = discord.Embed(title = "{}, you are not an Administrator".format(ctx.author), color = discord.Color.magenta())
            await ctx.send(embed = embed_not_admin)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed_miss_req_arg = discord.Embed(title = "Missing Required Arguments", color = discord.Color.magenta())
            embed_miss_req_arg.set_footer(text = "correct command: <prefix>delsub  <index value of subreddit>")
            await ctx.send(embed = embed_miss_req_arg)
        elif isinstance(error, commands.BadArgument):
            embed_correct_req_arg = discord.Embed(title = "Correct Required Argument", color = discord.Color.magenta())
            embed_correct_req_arg.set_footer(text = "correct command: <prefix>delsub  <index value of subreddit>")
            await ctx.send(embed = embed_correct_req_arg)
       
# Setup Cogs 'meme'
def setup(client):
    client.add_cog(meme(client))