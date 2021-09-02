# Imports
import discord
import random
from discord.ext import commands

# Create a class `games` which inherits from the `commands.Cog` class
class games(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Command for `coinflip` 
    coinflip_help ='''***Description :*** 
                            Tosses a fair coin\n
                            ***Syntax :***
                            `<prefix>coinflip`'''
    @commands.command(name ="coinflip", help = coinflip_help, aliases = ['cf', 'tosscoin', 'tc'])
    async def coinflip(self, ctx):
        cf_res = ['Heads', 'Tails']
        res = random.choice(cf_res)
        embed = discord.Embed(title = "Coinflip", description = f'Result = {res}!', 
        color = discord.Color.gold())
        await ctx.send(embed = embed)

    # Command for `die toss`
    tossdie_help ='''***Description :*** 
                            Tosses a fair die\n
                            ***Syntax :***
                            `<prefix>tossdie`'''
    @commands.command(name ="tossdie", help = tossdie_help, aliases = ['die', '6face'])
    async def tossdie(self, ctx):
        td_res = [int(i) for i in range(1,7)]
        res = random.choice(td_res)
        embed = discord.Embed(title = "Toss A Die", description = f'Result = {res}!',
        color = discord.Color.magenta())
        await ctx.send(embed = embed)

# Setup cogs `games`
def setup(client):
    client.add_cog(games(client))