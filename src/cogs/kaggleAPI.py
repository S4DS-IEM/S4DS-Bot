import discord

from discord import colour
from discord.ext import commands

from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

class KaggleAPI(commands.Cog):
    def __init__(self, client):
        self.client = client

        
    #Gets the entire list of competitions from Kaggle API and displays each competition including respective details
    @commands.command()
    async def list(self, ctx):
        listcomp = api.competitions_list_with_http_info(async_req = True)
        tup = listcomp.get()
        c = 0
        for submission in tup[0]:
            c += 1
            title = submission.get('title')
            url = submission.get('url')
            category = submission.get('category')
            description = submission.get('description')
            organizationName = submission.get('organizationName')
            reward = submission.get('reward')
            deadline = submission.get('deadline')
            teamCount = submission.get('teamCount')
            embed=discord.Embed(title = f'{title}', description = f'{description}', colour = discord.Colour.purple())
            embed.add_field(name = 'Category: ', value = category, inline = True)
            embed.add_field(name = 'Organisation: ', value = organizationName, inline = True)
            embed.add_field(name = 'Reward: ', value = reward, inline = False)
            embed.add_field(name = 'Deadline: ', value = deadline, inline = True)
            embed.add_field(name = 'Team Count: ', value=teamCount, inline = True)
            embed.add_field(name = 'Link: ', value = url, inline = False)
            await ctx.send(embed = embed)
            await ctx.send('.................................................................................................................................................')
        embed=discord.Embed(title = f'Displaying {c} search results for Kaggle Competitions.', colour = discord.Colour.gold())
        await ctx.send(embed = embed)



def setup(client):
    client.add_cog(KaggleAPI(client)) 
    
