# Imports
import os
import discord
from discord.ext import commands,tasks
import random
import json
from asyncpraw import Reddit
import asyncprawcore

# List of application-default subreddits
default_subred = ['DataScienceMemes', 'ProgrammerHumor', 'machinelearningmemes', 'mathmemes', 'linuxmemes', 'codingmemes', 'educationalmemes', 'applememes', 'windowsmemes']

#  Create a class 'meme' which inherits from the 'commands.Cog' class
class memes(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.subred_table_name = os.environ['SUBREDDITS_TABLE'] # subreddits list table name
        self.ap_table_name = os.environ['AUTOPOST_TABLE'] # autopost table name

    # Check if table and columns pertaining to autopost is present
    async def ap_table_check(self):
        # If doesn't exist, creates table pertaining to channels enabling autopost
        await self.client.pg_con.execute(f"CREATE TABLE IF NOT EXISTS {self.ap_table_name} (guild_id bigint NOT NULL, channel_id bigint NOT NULL, CONSTRAINT autopostlist_pkey PRIMARY KEY (guild_id), CONSTRAINT unique_channel UNIQUE (channel_id))")

        # If columns are deleted, to re-generate (with constraints)
        await self.client.pg_con.execute(f"ALTER TABLE IF EXISTS {self.ap_table_name} ADD COLUMN IF NOT EXISTS guild_id bigint NOT NULL CONSTRAINT autopostlist_pkey PRIMARY KEY")

        await self.client.pg_con.execute(f"ALTER TABLE IF EXISTS {self.ap_table_name} ADD COLUMN IF NOT EXISTS channel_id bigint NOT NULL CONSTRAINT unique_channel UNIQUE")

    # Check if table and columns pertaining to subreddits list is present
    async def subred_table_check(self):
        # If doesn't exist, creates table pertaining to list of subreddits for each guild
        await self.client.pg_con.execute(f"CREATE TABLE IF NOT EXISTS {self.subred_table_name}(guild_id bigint NOT NULL, subredlist character varying[] COLLATE pg_catalog.\"default\" NOT NULL, CONSTRAINT subredlist_pkey PRIMARY KEY (guild_id))")

        # If columns are deleted, to re-generate (with constraints)
        await self.client.pg_con.execute(f"ALTER TABLE IF EXISTS {self.subred_table_name} ADD COLUMN IF NOT EXISTS guild_id bigint NOT NULL CONSTRAINT subredlist_pkey PRIMARY KEY")

        await self.client.pg_con.execute(f"ALTER TABLE IF EXISTS {self.subred_table_name} ADD COLUMN IF NOT EXISTS subredlist character varying[] COLLATE pg_catalog.\"default\" NOT NULL")

    # Check if row pertaining to guild is present, which might not be the case if bot is invited when offline
    async def subred_row_check(self, ctx):
        subredlist = await self.client.pg_con.fetchrow(f"SELECT * from {self.subred_table_name} WHERE guild_id = $1", ctx.guild.id)
        if subredlist is None:
            await self.client.pg_con.execute(f"INSERT INTO {self.subred_table_name}(guild_id, subredlist) VALUES($1, $2) ON CONFLICT DO NOTHING", ctx.guild.id, default_subred)

    # 'Cog.listener' event which triggers autoposting in servers where it is enabled
    @commands.Cog.listener()
    async def on_ready(self):
        # Perform checks
        await self.ap_table_check() 
        await self.subred_table_check()
        # Start autopost loop
        await self.autopost.start()

    # Activating meme services on joining a server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.client.pg_con.execute(f"INSERT INTO {self.subred_table_name}(guild_id, subredlist) VALUES($1, $2) ON CONFLICT DO NOTHING", guild.id, default_subred)

    # Deactivating meme services and autoposting on leaving server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.client.pg_con.execute(f"DELETE FROM {self.subred_table_name} WHERE guild_id = $1 ", guild.id)
        await self.client.pg_con.execute(f"DELETE FROM {self.ap_table_name} WHERE guild_id = $1", guild.id)

    # Command for getting a meme
    meme_help ='''***Description :*** 
                            Command for getting a meme or a desired number of memes(not exceeding 5), based on user's wish\n
                            ***Syntax :***
                            `<prefix>memes <subreddit_index> <no.of_memes(limit=5)>`'''
    @commands.command(name ="meme", help = meme_help) 
    async def meme(self, ctx, arg : int, x = 1):
        credentials = json.loads(os.environ['REDDIT_CREDENTIALS'])
        
        async with Reddit(**credentials) as reddit:

            subredlist = await self.client.pg_con.fetchrow(f"SELECT * from {self.subred_table_name} WHERE guild_id = $1", ctx.guild.id)

            guild_id, sublist = subredlist

            if (x <= 5):
                if (arg > 0) and (arg <= len(sublist)):
                    subred = str(sublist[arg-1])
                    subreddit = await reddit.subreddit(subred)
                    all_meme = []
                        
                    hot = subreddit.hot(limit=500)
                    async for submission in hot:
                        all_meme.append(submission)
                        
                    for i in range(x):
                        random_meme = random.choice(all_meme)
                        name = str(random_meme.title)[:256:]
                        url = random_meme.url
                        author = random_meme.author
                        pst = "https://www.reddit.com" + random_meme.permalink
                        
                        embed = discord.Embed(title = name , url = pst, description = f'Created by u/{author}', colour = discord.Color.teal())
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

        embed = discord.Embed(title="Autoposting Enabled!", description=f"Now, memes will swarm channel `{channel.name}` every 15 minutes!", color=discord.Color.greyple())
        await ctx.send(embed=embed)

    # Command for ending AutoPost
    autopostoff_help = '''***Description :*** 
                            Command for ending AutoPost\n
                            ***Syntax :***
                            `<prefix>autopostoff`'''
    @commands.command(name ="autopostoff", help = autopostoff_help, aliases = ['apoff'])
    async def autopostoff(self, ctx):
        await self.client.pg_con.execute(f"DELETE FROM {self.ap_table_name} WHERE guild_id = $1", ctx.guild.id)

        embed = discord.Embed(title="Autoposting Disabled!", description=f"Autoposting disabled for the server!", color=discord.Color.greyple())
        await ctx.send(embed=embed)

    # Loop for autoposting every 15 minutes
    @tasks.loop(minutes=15)
    async def autopost(self):
        credentials = json.loads(os.environ['REDDIT_CREDENTIALS'])
        
        async with Reddit(**credentials) as reddit:

            random_sub = random.choice(default_subred)

            subreddit = await reddit.subreddit(random_sub)
            all_meme = []
            hot = subreddit.hot(limit=500)
            async for submission in hot:
                all_meme.append(submission)
            random_meme = random.choice(all_meme)
            name = str(random_meme.title)[:256:]
            url = random_meme.url
            author = random_meme.author
            pst = "https://www.reddit.com" + random_meme.permalink

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
        await self.subred_row_check(ctx)

        subredlist = await self.client.pg_con.fetchrow(f"SELECT * from {self.subred_table_name} WHERE guild_id = $1", ctx.guild.id)

        guild_id, sublist = subredlist

        templist = []

        for x in range(1,(len(sublist)+1)):
            m = str(x) + f'.  r/{sublist[x-1]}' + '\n'
            templist.append(m)
        templist[-1] = templist[-1].strip('\n')
        meme_list = ''.join(templist)
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
    async def addsub(self, ctx, subreddit_name):
        await self.subred_row_check(ctx)

        # Setup API Client
        credentials = json.loads(os.environ['REDDIT_CREDENTIALS'])
        async with Reddit(**credentials) as reddit:
        
            if subreddit_name.startswith(('/r/', 'r/')):
                subreddit_name = subreddit_name.split('r/')[-1] # -1 gets the last element in the list
            try:
                # Check if subreddit is valid
                subreddit_chk = await reddit.subreddit(subreddit_name, fetch=True) # by default Async PRAW doesn't make network requests when subreddit is called

                # Fetch original list of subreddits for server
                subredlist = await self.client.pg_con.fetchrow(f"SELECT * from {self.subred_table_name} WHERE guild_id = $1", ctx.guild.id)

                guild_id, sublist = subredlist

                sublist.append(subreddit_name)

                await self.client.pg_con.execute(f"UPDATE {self.subred_table_name} SET subredlist = $2 WHERE guild_id = $1", ctx.guild.id, sublist)

                templist = []

                for x in range(1, (len(sublist)+1)):
                    m = str(x) + f'.  r/{sublist[x-1]}' + '\n'
                    templist.append(m)
                templist[-1] = templist[-1].strip('\n')
                meme_list = ''.join(templist)
                embed = discord.Embed(title = "Subreddit Added Successfully", color = discord.Color.blue(), inline = False)
                embed.add_field(name = "Updated Subreddit List:\n", value = f"{meme_list}" , inline = False)
                
            except asyncprawcore.Redirect: 
                # Reddit will redirect to reddit.com/search if the subreddit doesn't exist
                embed = discord.Embed(title = f"Invalid Subreddit!", description = f"Subreddit `{subreddit_name}` doesn't exist!", color = discord.Color.magenta())

            await ctx.send(embed=embed)

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
        await self.subred_row_check(ctx)
        
        # Fetch original list of subreddits for server
        subredlist = await self.client.pg_con.fetchrow(f"SELECT * from {self.subred_table_name} WHERE guild_id = $1", ctx.guild.id)

        guild_id, sublist = subredlist

        # Check if index of argument is within the range of index of subreddits
        if (m>0) and (m<=len(sublist)):

            # If yes, remove subreddit whose index has been passed as argument
            sublist.pop(m-1)

            # Update the new value in the corresponding row in table
            await self.client.pg_con.execute(f"UPDATE {self.subred_table_name} SET subredlist = $2 WHERE guild_id = $1", ctx.guild.id, sublist)

            templist = []
            for x in range(1, (len(sublist)+1)):
                m = str(x) + f'.  r/{sublist[x-1]}' + '\n'
                templist.append(m)
            templist[-1] = templist[-1].strip('\n')
            meme_list = ''.join(templist)
            embed = discord.Embed(title = "Subreddit Deleted Successfully", color = discord.Color.blue(), inline = False)
            embed.add_field(name = "Updated Subreddit List:\n", value = f"{meme_list}" , inline = False)
            await ctx.send(embed = embed)

        else:
            embed_inc_index= discord.Embed(title="Incorrect Index", 
            description = f"We only have {len(sublist)} subreddits enlisted in our Subreddit List. \nTrigger the <sublist> command for getting correct Subreddit list" , 
            color = discord.Color.blue(), inline=False)
            await ctx.send(embed= embed_inc_index)

    # Error handling for 'meme' command
    @meme.error
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
    client.add_cog(memes(client))