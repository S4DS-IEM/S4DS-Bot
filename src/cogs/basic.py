import discord
from discord.enums import Status 
from discord.ext import commands, tasks
from itertools import cycle
import asyncio

status = cycle(['arXiv','Kaggle','redditAPI'])

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

    @commands.command()
    async def ping(self, ctx):
        embed=discord.Embed(title="Ping",
        description=f'Pong! In {round(self.client.latency*1000)} ms.',
        color=discord.Color.green())
        embed.set_footer(text=f'Information requested by : {ctx.author.display_name}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)
        embed=discord.Embed(title="Purged Messages!",description=f'{amount} messages have been cleared.',
        color=discord.Color.teal())
        await ctx.send(embed=embed)
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)

    @clear.error
    async def on_command_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed_title="Missing Required Argument!"
            embed_desc="Please specify an amount of messages to be deleted!"
            embed_color=discord.Color.orange()
            #await ctx.send('Please specify an amount of messages to be deleted!')
        elif isinstance(error, commands.MissingPermissions):
            embed_title="Missing Permissions!"
            embed_desc="Missing `Manage Messages` Permissions!"
            embed_color=discord.Color.red()
            #await ctx.send('Missing `Manage Messages` Permissions!')
        else:
            return
        embed=discord.Embed(title=embed_title,description=embed_desc,color=embed_color)
        embed.set_footer(text=f'Command error encountered by : {ctx.author.display_name}')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(basic(client))

    