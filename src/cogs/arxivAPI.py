import discord
import urllib, urllib.request
from xml.dom import minidom
    
from discord.ext import commands

class arxivapi(commands.Cog):
    def __init__(self, client):
        self.client = client


    #Gets the top search result from arXiv API and displays the paper along with related details (including summary) in an embed  
    arxivshow_help ='''***Description :*** 
                            Shows the top searched result\n
                            ***Syntax :***
                            `<prefix>arxivshow <keyword>`'''
    @commands.command(name ="arxivshow", help = arxivshow_help)
    async def arxivshow(self, ctx, *, search):
        query = search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1'
        data = urllib.request.urlopen(url)
        mytree = minidom.parseString(data.read().decode('utf-8'))
        entry = mytree.getElementsByTagName('entry')
        for y in entry:
            published = y.getElementsByTagName('published')[0]
            title = y.getElementsByTagName('title')[0]
            summary = y.getElementsByTagName('summary')[0]
            author = y.getElementsByTagName('author')
            authors = ''
            for x in author:
                a_name = x.getElementsByTagName('name')[0]
                authors = authors + (a_name.firstChild.data) + ', '
            authors = authors[:-2]
            link = y.getElementsByTagName('link')[0]
            link1 = link.attributes['href'].value
            link2 = y.getElementsByTagName('link')[1]
            link3 = link2.attributes['href'].value
            embed = discord.Embed(title = f'Title: {title.firstChild.data}', description = f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name = f'{authors}')
            await ctx.send(embed = embed)
            embed = discord.Embed(title = 'Summary: ', description = f'{summary.firstChild.data}', color = discord.Colour.green())
            embed.add_field(name = 'Link: ', value = f'{link1}', inline = False)
            embed.add_field(name = 'Download link: ', value = f'{link3}', inline = False)
            await ctx.send(embed = embed)
            await ctx.send('.................................................................................................................................................')

    #Gets the top 5 search results (sorted as last updated) from arXiv API and displays respective papers along with related details (excluding summary) in succesive embeds  
    arxivshowlud_help ='''***Description :*** 
                            Shows top 5 paper on the basis of last updated date\n
                            ***Syntax :***
                            `<prefix>arxivshowlud <keyword>`'''
    @commands.command(name ="arxivshowlud", help = arxivshowlud_help)
    async def arxivshowlud(self, ctx, *, search):
        query = search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=lastUpdatedDate&sortOrder=ascending'
        data = urllib.request.urlopen(url)
        mytree = minidom.parseString(data.read().decode('utf-8'))
        entry = mytree.getElementsByTagName('entry')
        for y in entry:
            published = y.getElementsByTagName('published')[0]
            title = y.getElementsByTagName('title')[0]
            author = y.getElementsByTagName('author')
            authors = ''
            for x in author:
                a_name = x.getElementsByTagName('name')[0]
                authors = authors + (a_name.firstChild.data) + ', '
            authors = authors[:-2]
            link = y.getElementsByTagName('link')[0]
            link1 = link.attributes['href'].value
            link2 = y.getElementsByTagName('link')[1]
            link3 = link2.attributes['href'].value
            embed = discord.Embed(title = f'Title: {title.firstChild.data}', description = f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name = f'{authors}')
            embed.add_field(name = 'Link: ', value = f'{link1}', inline = False)
            embed.add_field(name = 'Download link: ', value = f'{link3}', inline = False)
            await ctx.send(embed = embed)
            await ctx.send('.................................................................................................................................................')

    #Gets the top 5 search results (sorted as relevance) from arXiv API and displays respective papers along with related details (excluding summary) in succesive embeds
    arxivshowr_help ='''***Description :*** 
                            Shows top 5 paper on the basis of relevance\n
                            ***Syntax :***
                            `<prefix>arxivshowr <keyword>`'''
    @commands.command(name ="arxivshowr", help = arxivshowr_help)
    async def arxivshowr(self, ctx, *, search):
        query = search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=relevance&sortOrder=ascending'
        data = urllib.request.urlopen(url)
        mytree = minidom.parseString(data.read().decode('utf-8'))
        entry = mytree.getElementsByTagName('entry')
        for y in entry:
            published = y.getElementsByTagName('published')[0]
            title = y.getElementsByTagName('title')[0]
            author = y.getElementsByTagName('author')
            authors = ''
            for x in author:
                a_name = x.getElementsByTagName('name')[0]
                authors = authors+(a_name.firstChild.data) + ', '
            authors = authors[:-2]
            link = y.getElementsByTagName('link')[0]
            link1 = link.attributes['href'].value
            link2 = y.getElementsByTagName('link')[1]
            link3 = link2.attributes['href'].value
            embed = discord.Embed(title = f'Title: {title.firstChild.data}', description = f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name = f'{authors}')
            embed.add_field(name = 'Link: ', value = f'{link1}', inline = False)
            embed.add_field(name = 'Download link: ', value = f'{link3}', inline = False)
            await ctx.send(embed = embed)
            await ctx.send('.................................................................................................................................................')

    #Gets the top 5 search results (sorted as submitted date) from arXiv API and displays respective papers along with related details (excluding summary) in succesive embeds
    arxivshowsd_help ='''***Description :*** 
                            Shows top 5 paper and sorts the result in order of submitted date\n
                            ***Syntax :***
                            `<prefix>arxivshowsd <keyword>`'''
    @commands.command(name="arxivshowsd", help=arxivshowsd_help)
    async def arxivshowsd(self, ctx, *, search):
        query = search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=ascending'
        data = urllib.request.urlopen(url)
        mytree = minidom.parseString(data.read().decode('utf-8'))
        entry = mytree.getElementsByTagName('entry')
        for y in entry:
            published = y.getElementsByTagName('published')[0]
            title = y.getElementsByTagName('title')[0]
            author = y.getElementsByTagName('author')
            authors = ''
            for x in author:
                a_name = x.getElementsByTagName('name')[0]
                authors = authors + (a_name.firstChild.data) + ', '
            authors = authors[:-2]
            link = y.getElementsByTagName('link')[0]
            link1 = link.attributes['href'].value
            link2 = y.getElementsByTagName('link')[1]
            link3 = link2.attributes['href'].value
            embed = discord.Embed(title = f'Title: {title.firstChild.data}', description = f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name = f'{authors}')
            embed.add_field(name = 'Link: ', value = f'{link1}', inline = False)
            embed.add_field(name = 'Download link: ', value = f'{link3}', inline = False)
            await ctx.send(embed = embed)
            await ctx.send('.................................................................................................................................................')

    #Gets the top 5 search results from arXiv API and displays respective papers along with related details (including summary) in succesive embeds
    arxivshowsumm_help ='''***Description :*** 
                            Shows top 5 paper alongwith it's summary\n
                            ***Syntax :***
                            `<prefix>arxivshowsumm <keyword>`'''   
    @commands.command(name ="arxivshowsumm", help = arxivshowsumm_help)
    async def arxivshowsumm(self, ctx, *, search):
        query = search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5'
        data = urllib.request.urlopen(url)
        mytree = minidom.parseString(data.read().decode('utf-8'))
        entry = mytree.getElementsByTagName('entry')
        for y in entry:
            published = y.getElementsByTagName('published')[0]
            title = y.getElementsByTagName('title')[0]
            author = y.getElementsByTagName('author')
            authors = ''
            for x in author:
                a_name = x.getElementsByTagName('name')[0]
                authors = authors + (a_name.firstChild.data) + ', '
            authors = authors[:-2]
            summary = y.getElementsByTagName('summary')[0]
            link = y.getElementsByTagName('link')[0]
            link1 = link.attributes['href'].value
            link2 = y.getElementsByTagName('link')[1]
            link3 = link2.attributes['href'].value
            embed = discord.Embed(title = f'Title: {title.firstChild.data}', description = f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name = f'{authors}')
            await ctx.send(embed = embed)
            embed = discord.Embed(title = 'Summary: ', description = f'{summary.firstChild.data}', color = discord.Colour.green())
            embed.add_field(name = 'Link: ', value = f'{link1}', inline = False)
            embed.add_field(name = 'Download link: ', value = f'{link3}', inline = False)
            await ctx.send(embed = embed)
            await ctx.send('.................................................................................................................................................')


def setup(client):
    client.add_cog(arxivapi(client)) 