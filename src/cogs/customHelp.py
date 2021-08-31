from os import name
import discord 
from discord.ext import commands
from discord.ext.commands.core import command

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client=commands.Bot(command_prefix=',',intents=intents)
client.remove_command("help")


class Help(commands.Cog):
    def __init__(self,client):
        self.client=client

    # Customized help command to show all the functionalitites present in the bot 
    @client.group(invoke_without_command = True)
    #@client.command()
    async def help(self,ctx):
        embed = discord.Embed(title = "Help", description = "Use -help command for information on the commands", color = ctx.author.color)
        embed.add_field(name = "arXiv-API", value = "arxivshow\narxivshowlud\narxivshowr\narxivshowsd\narxivshowsumm\nType <prefix>help arxiv\nto view all functions")
        embed.add_field(name = "reddit-API", value = "memes\nautoposton\nautopostoff\nsublist\naddsub\ndelsub\nType <prefix>help reddit\nto view all the functions", inline=True)
        embed.add_field(name = "Kaggle", value = "list", inline = False)
        embed.add_field(name = "Admin commands", value = "load\nunload\nreload\nType <prefix>help Admin to view all the functions", inline = False)
        embed.add_field(name = "Basic", value = "clear\nping\nsetprefix", inline = True)
        embed.add_field(name = "games", value = "coinflip\ntossdie", inline = True)
        await ctx.send(embed = embed)
        
    # Segment of help command to be called when user wishes to view the arxivshow functionality under the arXiv heading
    @help.command()
    async def arxivshow(self, ctx):
        embed = discord.Embed(title = "arxivshow", description = "displays the top result with summary using the searched keyword", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix> arxivshow <keyword>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the arxivshowlud functionality under the arXiv heading
    @help.command()
    async def arxivshowlud(self, ctx):
        embed = discord.Embed(title = "arxivshowlud", description = "displays top 5 papers and sorts the result on the basis of last updated date", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix> arxivshowlud <keyword>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the arxivshowr functionality under the arXiv heading
    @help.command()
    async def arxivshowr(self, ctx):
        embed = discord.Embed(title = "arxivshowr", description = "displays top 5 papers and sorts the result on the basis of relevance", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix> arxivshowr <keyword>")
        await ctx.send(embe = embed)

    # Segment of help command to be called when user wishes to view the arxivshowsd functionality under the arXiv heading
    @help.command()
    async def arxivshowsd(self, ctx):
        embed = discord.Embed(title = "arxivshowsd", description = "displays top 5 papers and sorts the result on the basis of submitted date", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix> arxivshowsd <keyword>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the arxivshowsumm functionality under the arXiv heading
    @help.command()
    async def arxivshowsumm(self, ctx):
        embed = discord.Embed(title = "arxivshowsumm", description = "displays top 5 papers alongwith respectives summaries", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix> arxivshowsumm <keyword>")
        await ctx.send(embed = embed)

    # Segment of help command to return all of the functionalities under arXiv-API
    @help.command()
    async def arxiv(self, ctx):
        embed = discord.Embed(title = "arXiv-API", description = "class to access research paper under arXiv.org", color = ctx.author.color)
        embed.add_field(name = "arxivshow", value = "displays the top result with summary using the searched keyword", inline = False)
        embed.add_field(name = "arxivshowlud", value = "displays top 5 papers and sorts the result on the basis of last updated date", inline = False)
        embed.add_field(name = "arxivshowr", value = "displays top 5 papers and sorts the result on the basis of relevance", inline = False)
        embed.add_field(name = "arxivshowsd", value = "displays top 5 papers and sorts the result on the basis of submitted date", inline = False)
        embed.add_field(name = "arxivshowsumm", value = "displays top 5 papers alongwith respectives summaries", inline = False)
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the meme functionality 
    @help.command()
    async def memes(self,ctx):
        desc = '''Displays a certain no. of memes from an index passed an argument from a pre-
        determined list of subreddits, by default 1 and a maximum of 5 at a time.
        The <no._of_memes> is an optional argument as such.
        Returns error if :
        i. No subreddit index is passed as argument. 
        ii. Invalid subreddit index is passed as argument. 
        iii. The no. of requested memes is more than 5 at a time.'''
        embed = discord.Embed(title = "memes", description = desc, color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>memes <subreddit_index> <no.of_memes(limit=5)>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the autoposton functionality 
    @help.command()
    async def autoposton(self,ctx):
        embed = discord.Embed(title = "autoposton", description = "Posts a meme in the specified channel passed as argument at regular intervals (by default 15 minutes) at coordinated time for all servers.", color = ctx.author.color)
        embed.add_field(name = "Aliases:", value = "['apon']")
        embed.add_field(name = "**Syntax**", value = "<prefix>autoposton <channel>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the autopostoff functionality 
    @help.command()
    async def autopostoff(self,ctx):
        embed = discord.Embed(title = "autopostoff", description = "Turns off autoposting for the channel where it is enabled in a server.", color = ctx.author.color)
        embed.add_field(name = "Aliases:", value = "['apoff']")
        embed.add_field(name = "**Syntax**", value = "<prefix>autopostoff <channel>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the autoposton functionality 
    @help.command()
    async def sublist(self,ctx):
        embed = discord.Embed(title = "sublist", description = "Shows a list of available subreddits.", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>sublist")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the autoposton functionality 
    @help.command()
    async def addsub(self,ctx):
        embed = discord.Embed(title = "addsub", description = "Adds a subreddit to the list of existing subreddits.", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>addsub <subreddit_name>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the list functionality under the Kaggle heading
    @help.command()
    async def delsub(self, ctx):
        embed = discord.Embed(title = "delsub", description = "Deletes a subreddit to the list of existing subreddits", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>delsub <index>")
        await ctx.send(embed = embed)

    # Segment of help command to return all of the functionalities under reddit-API
    @help.command()
    async def reddit(self, ctx):
        embed = discord.Embed(title = "reddit-API", description = "class to access the memes in reddit", color = ctx.author.color)
        embed.add_field(name = "memes", value = "displays a certain no. of memes from an index passed an argument from a pre-determined list of subreddits, by default 1 and a maximum of 5 at a time.", inline = False)
        embed.add_field(name = "autoposton", value = "posts a meme in the specified channel passed as argument at regular intervals (by default 15 minutes) at coordinated time for all servers.", inline = False)
        embed.add_field(name = "autopostoff", value = "turns off autoposting for the channel where it is enabled in a server.", inline = False)
        embed.add_field(name = "sublist", value = "shows a list of available subreddits", inline = False)
        embed.add_field(name = "addsub", value = "adds a subreddit to the list of existing subreddits", inline = False)
        embed.add_field(name = "delsub", value = "removes subreddit at index passed as argument.", inline = False)
        await ctx.send(embed = embed)
    
    # Segment of help command to be called when user wishes to view the Kaggle class 
    @help.command()
    async def Kaggle(self, ctx):
        embed = discord.Embed(title = "Kaggle", description = "class to access Kaggle website", color = ctx.author.color)
        await ctx.send(embed = embed)
    
    # Segment of help command to be called when user wishes to view the load functionality under the Kaggle class
    @help.command()
    async def list(self, ctx):
        embed = discord.Embed(title = "list", description = "Displays top 20 competitions from Kaggle Competition List ", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>list")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the load functionality under the Admin commands heading
    @help.command()
    async def load(self, ctx):
        embed = discord.Embed(title = "load(for Admins)", description = "Loads a segment of the program\nThere are classes with names 'arxivAPI', 'kaggleAPI', 'redditAPI', 'basic', 'games', and 'customHelp' ", color = ctx.author.color)
        embed.add_field(name="Perms Required:", description = "Administrator")
        embed.add_field(name = "**Syntax**", value = "<prefix>load <class name>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the load functionality under the Admin commands heading
    @help.command()
    async def unload(self, ctx):
        embed = discord.Embed(title = "unload(for Admins)", description = "Unloads a segment of the program\nThere are classes with names 'arxivAPI', 'kaggleAPI', 'redditAPI', 'basic', 'games', and 'customHelp' ", color = ctx.author.color)
        embed.add_field(name="Perms Required:", description = "Administrator")
        embed.add_field(name = "**Syntax**", value = "<prefix>unload <class name>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the load functionality under the Admin commands heading
    @help.command()
    async def reload(self, ctx):
        embed = discord.Embed(title = "reload(for Admins)", description = "Reloads a segment of the program\nThere are classes with names 'arxivAPI', 'kaggleAPI', 'redditAPI', 'basic', 'games', and 'customHelp' ", color = ctx.author.color)
        embed.add_field(name="Perms Required:", description = "Administrator")
        embed.add_field(name = "**Syntax**", value = "<prefix>reload <class name>")
        await ctx.send(embed = embed)

    # Segment of help command to return all of the functionalities under Admin commands
    @help.command()
    async def Admin(self, ctx):
        embed = discord.Embed(title = "Admin commands", description = "only accessible by admins of the group", color = ctx.author.color)
        embed.add_field(name = "load", value = "Loads a segment of the program\nThere are classes with names 'arxivAPI', 'kaggleAPI', 'redditAPI', 'basic', 'games', and 'customHelp'", inline = False)
        embed.add_field(name = "unload", value = "Unloads a segment of the program\nThere are classes with names 'arxivAPI', 'kaggleAPI', 'redditAPI', 'basic', 'games', and 'customHelp'", inline = False)
        embed.add_field(name = "autopostoff", value = "Reloads a segment of the program\nThere are classes with names 'arxivAPI', 'kaggleAPI', 'redditAPI', 'basic', 'games', and 'customHelp'", inline = False)
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the clear functionality under the Basic heading
    @help.command()
    async def clear(self, ctx):
        embed = discord.Embed(title = "clear", description = "used to clear messages (admin permission)", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>clear <frequency>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the ping functionality under the Basic heading
    @help.command()
    async def ping(self, ctx):
        embed = discord.Embed(title = "ping", description = "returns the latency of the client in ms", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>ping")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the setprefix functionality under the Basic heading
    @help.command()
    async def setprefix(self, ctx):
        embed = discord.Embed(title = "setprefix", description = "changes the prefix to user defined prefix", color = ctx.author.color)
        embed.add_field(name = "**Syntax**", value = "<prefix>setprefix <keyword>")
        await ctx.send(embed = embed)

    # Segment of help command to be called when user wishes to view the clear functionality under the games heading
    @help.command()
    async def coinflip(self, ctx):
        embed = discord.Embed(title = "coinflip", description = "randomly returns heads or tails", color = ctx.author.color)
        embed.add_field(name = "Aliases", value="['cf', 'tosscoin', 'tc']")
        embed.add_field(name = "**Syntax**", value = "<prefix>coinflip")
        await ctx.send(embed = embed)
    
    # Segment of help command to be called when user wishes to view the clear functionality under the games heading
    @help.command()
    async def tossdie(self, ctx):
        embed = discord.Embed(title = "tossdie", description = "returns a random throw of die ranging from 1 to 6", color = ctx.author.color)
        embed.add_field(name = "Aliases", value="['die', '6face']")
        embed.add_field(name = "**Syntax**", value = "<prefix>tossdie")
        await ctx.send(embed = embed)

# Setup Cogs 'customHelp'
def setup(client):
    client.add_cog(Help(client)) 