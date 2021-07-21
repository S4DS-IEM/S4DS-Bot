import discord
import random
from discord.ext import commands

class games(commands.Cog):
    def __init__(self, client):
        self.client=client

    '''@commands.Cog.listener()
    async def on_ready(self):
        print("Bot is onlyn")'''
    
    @commands.command(aliases = ['cf','tosscoin','tc'])
    async def coinflip(self, ctx):
        cf_res = ['Heads','Tails']
        await ctx.send(f'{random.choice(cf_res)}')

    @commands.command(aliases = ['die','6face'])
    async def tossdie(self, ctx):
        td_res = [int(i) for i in range(1,7)]
        await ctx.send(f'{random.choice(td_res)}')

def setup(client):
    client.add_cog(games(client))