# Imports
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
import asyncio

# Cycle which consists of the bot statuses to be cycled through at regular intervals
status = cycle(['arXiv', 'Kaggle', 'redditAPI'])

# Create a class `basic` which inherits from the `commands.Cog` class
class basic(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pref_table = os.environ['PREFIXES_TABLE'] # Table for prefixes

    # Event (Cog.listener()) event which prints online status of bot on console 
    # and triggers status/activity cycle of bot
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Status : Online") 

    # Setting prefix as default on joining a server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.client.pg_con.execute(f"INSERT INTO {self.pref_table}(server_id, server_prefix) VALUES($1, $2) ON CONFLICT DO NOTHING", guild.id, '.')

    # Deleting prefix on leaving server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.client.pg_con.execute(f"DELETE FROM {self.pref_table} WHERE server_id = $1", guild.id)

    # Returns prefix for server on being mentioned
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            server_id, server_prefix = await self.client.pg_con.fetchrow(f"SELECT * FROM {self.pref_table} WHERE server_id = $1", message.guild.id)
            embed = discord.Embed(title="Server Prefix", description=f"The prefix for this server is `{server_prefix}` !", color=discord.Color.orange())
            await message.channel.send(embed=embed)

    # Command to assign custom prefix
    setprefix_help = '''***Description :*** 
                            Changes bot prefix to new string passed as argument\n
                            ***Syntax :***
                            `<prefix>setprefix <new_prefix>` \n
                            ***Constraints :***
                            `Max Length : 5` \n
                            **Permissions Required :**
                            `Administrator`'''
    @commands.command(name ="setprefix", help = setprefix_help)
    @commands.has_permissions(administrator = True)
    async def setprefix(self, ctx, prefix):
        
        if isinstance(prefix, str) and len(prefix)>0 and len(prefix)<=5:
            await self.client.pg_con.execute(f"UPDATE {self.pref_table} SET server_prefix = $2 WHERE server_id = $1", ctx.guild.id, prefix)
            embed = discord.Embed(title="Prefix changed!", description=f'Prefix changed to `{prefix}` !', color=discord.Color.orange())    
        else:
            embed = discord.Embed(title="Invalid Prefix!", description=f'Please use a prefix of length between 1 and 5 characters!', color=discord.Color.dark_red())    
             
        await ctx.send(embed=embed)
                     
    # Loop that cycles bot status at every 15 seconds
    @tasks.loop(seconds = 30)
    async def change_status(self):
        await self.client.change_presence(activity = discord.Game(next(status)))

    # Command that returns latency of the client in channel where it is triggered
    ping_help ='''***Description :*** 
                            Returns the latency of the user or the client in ms\n
                            ***Syntax :***
                            `<prefix>ping`'''
    @commands.command(name ="ping", help = ping_help)
    async def ping(self, ctx):
        embed = discord.Embed(title = "Ping",
        description = f'Pong! In {round(self.client.latency*1000)} ms.',
        color = discord.Color.green())
        embed.set_footer(text = f'Information requested by : {ctx.author.display_name}')
        await ctx.send(embed = embed)

    # Command that deletes a specified number of messages from the channel 
    # where it is triggered
    clear_help ='''***Description :*** 
                            Clears a certain amount of messages from the channel\n
                            ***Syntax :***
                            `<prefix>clear <limit>`\n
                            ***Limit :***
                            `50`'''
    @commands.command(name ="clear", help = clear_help)
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount : int):
        if amount>0 and amount<=50:
            await ctx.channel.purge(limit = amount + 1)
            embed = discord.Embed(title = "Purged Messages!", description = f'{amount} messages have been cleared.',
            color = discord.Color.dark_blue())
        else:
            embed = discord.Embed(title = "Invalid Limits!", description = f'Please enter a valid limit between 1 and 50!',
            color = discord.Color.magenta())
        await ctx.send(embed = embed)
        await asyncio.sleep(2)
        await ctx.channel.purge(limit = 1)

    # Error message displayed in discord channel in case invalid command is entered
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title = "Invalid Command!", description = "Command Not Found!",
            color = discord.Color.dark_red())
            await ctx.send(embed = embed)
    
    # Error handler for 'setprefix' command
    @setprefix.error
    async def on_command_err(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed_title = "Missing Permissions!"
            embed_desc = "Missing `Administrator` Permissions!"
            embed_color = discord.Color.red()
        embed = discord.Embed(title = embed_title, description = embed_desc, 
        color = embed_color)
        embed.set_footer(text = f'Command error encountered by : {ctx.author.display_name}')
        await ctx.send(embed = embed)

    # Error handler for `clear` command
    @clear.error
    async def on_command_err(self, ctx, error):
        # Error displayed in text channel when required argument is not provided
        if isinstance(error, commands.MissingRequiredArgument):
            embed_title = "Missing Required Argument!"
            embed_desc = "Please specify an amount of messages to be deleted!"
            embed_color = discord.Color.orange()
        
        # Error displayed in text channel when user does not have permissions required
        # to trigger the command
        elif isinstance(error, commands.MissingPermissions):
            embed_title = "Missing Permissions!"
            embed_desc = "Missing `Manage Messages` Permissions!"
            embed_color = discord.Color.red()
        else:
            return
        embed = discord.Embed(title = embed_title, description = embed_desc, 
        color = embed_color)
        embed.set_footer(text = f'Command error encountered by : {ctx.author.display_name}')
        await ctx.send(embed = embed)

# Setup cogs `basic`
def setup(client):
    client.add_cog(basic(client))

    