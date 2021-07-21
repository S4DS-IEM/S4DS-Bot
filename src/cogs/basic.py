import discord
from discord.enums import Status 
from discord.ext import commands, tasks
from itertools import cycle

status = cycle(['arXiv','Kaggle'])

class basic(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Bot is ready")

    @tasks.loop(seconds=15)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid Command!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! In {round(self.client.latency*1000)} ms.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def on_command_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to be deleted!')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Missing ```Manage Messages``` Permissions!')


def setup(client):
    client.add_cog(basic(client))

    