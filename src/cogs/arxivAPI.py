import discord
import urllib, urllib.request
from xml.dom import minidom
    
from discord.ext import commands

class ArxivAPI(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def arxivshow(self,ctx,*,search):
        query=search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1'
        data = urllib.request.urlopen(url)
        mytree=minidom.parseString(data.read().decode('utf-8'))
        entry=mytree.getElementsByTagName('entry')
        for y in entry:
            published=y.getElementsByTagName('published')[0]
            title=y.getElementsByTagName('title')[0]
            summary=y.getElementsByTagName('summary')[0]
            author=y.getElementsByTagName('author')
            authors=''
            for x in author:
                a_name=x.getElementsByTagName('name')[0]
                authors=authors+(a_name.firstChild.data)+', '
            authors=authors[:-2]
            link=y.getElementsByTagName('link')[0]
            link1=link.attributes['href'].value
            link2=y.getElementsByTagName('link')[1]
            link3=link2.attributes['href'].value
            embed=discord.Embed(title= f'Title: {title.firstChild.data}', description= f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name=f'{authors}')
            await ctx.send(embed=embed)
            embed=discord.Embed(title='Summary: ', description= f'{summary.firstChild.data}', color = discord.Colour.green())
            embed.add_field(name='Link: ', value=f'{link1}', inline=False)
            embed.add_field(name='Download link: ', value=f'{link3}', inline=False)
            await ctx.send(embed=embed)
            await ctx.send('.................................................................................................................................................')

    @commands.command()
    async def arxivshowlud(self,ctx,*,search):
        query=search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=lastUpdatedDate&sortOrder=ascending'
        data = urllib.request.urlopen(url)
        mytree=minidom.parseString(data.read().decode('utf-8'))
        entry=mytree.getElementsByTagName('entry')
        for y in entry:
            published=y.getElementsByTagName('published')[0]
            title=y.getElementsByTagName('title')[0]
            author=y.getElementsByTagName('author')
            authors=''
            for x in author:
                a_name=x.getElementsByTagName('name')[0]
                authors=authors+(a_name.firstChild.data)+', '
            authors=authors[:-2]
            link=y.getElementsByTagName('link')[0]
            link1=link.attributes['href'].value
            link2=y.getElementsByTagName('link')[1]
            link3=link2.attributes['href'].value
            embed=discord.Embed(title= f'Title: {title.firstChild.data}', description= f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name=f'{authors}')
            embed.add_field(name='Link: ', value=f'{link1}', inline=False)
            embed.add_field(name='Download link: ', value=f'{link3}', inline=False)
            await ctx.send(embed=embed)
            await ctx.send('.................................................................................................................................................')

    @commands.command()
    async def arxivshowr(self,ctx,*,search):
        query=search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=relevance&sortOrder=ascending'
        data = urllib.request.urlopen(url)
        mytree=minidom.parseString(data.read().decode('utf-8'))
        entry=mytree.getElementsByTagName('entry')
        for y in entry:
            published=y.getElementsByTagName('published')[0]
            title=y.getElementsByTagName('title')[0]
            author=y.getElementsByTagName('author')
            authors=''
            for x in author:
                a_name=x.getElementsByTagName('name')[0]
                authors=authors+(a_name.firstChild.data)+', '
            authors=authors[:-2]
            link=y.getElementsByTagName('link')[0]
            link1=link.attributes['href'].value
            link2=y.getElementsByTagName('link')[1]
            link3=link2.attributes['href'].value
            embed=discord.Embed(title= f'Title: {title.firstChild.data}', description= f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name=f'{authors}')
            embed.add_field(name='Link: ', value=f'{link1}', inline=False)
            embed.add_field(name='Download link: ', value=f'{link3}', inline=False)
            await ctx.send(embed=embed)
            await ctx.send('.................................................................................................................................................')

    @commands.command()
    async def arxivshowsd(self,ctx,*,search):
        query=search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=ascending'
        data = urllib.request.urlopen(url)
        mytree=minidom.parseString(data.read().decode('utf-8'))
        entry=mytree.getElementsByTagName('entry')
        for y in entry:
            published=y.getElementsByTagName('published')[0]
            title=y.getElementsByTagName('title')[0]
            author=y.getElementsByTagName('author')
            authors=''
            for x in author:
                a_name=x.getElementsByTagName('name')[0]
                authors=authors+(a_name.firstChild.data)+', '
            authors=authors[:-2]
            link=y.getElementsByTagName('link')[0]
            link1=link.attributes['href'].value
            link2=y.getElementsByTagName('link')[1]
            link3=link2.attributes['href'].value
            embed=discord.Embed(title= f'Title: {title.firstChild.data}', description= f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name=f'{authors}')
            embed.add_field(name='Link: ', value=f'{link1}', inline=False)
            embed.add_field(name='Download link: ', value=f'{link3}', inline=False)
            await ctx.send(embed=embed)
            await ctx.send('.................................................................................................................................................')

    @commands.command()
    async def arxivshowsumm(self,ctx,*,search):
        query=search.replace(" ", "+")
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5'
        data = urllib.request.urlopen(url)
        mytree=minidom.parseString(data.read().decode('utf-8'))
        entry=mytree.getElementsByTagName('entry')
        for y in entry:
            published=y.getElementsByTagName('published')[0]
            title=y.getElementsByTagName('title')[0]
            author=y.getElementsByTagName('author')
            authors=''
            for x in author:
                a_name=x.getElementsByTagName('name')[0]
                authors=authors+(a_name.firstChild.data)+', '
            authors=authors[:-2]
            summary=y.getElementsByTagName('summary')[0]
            link=y.getElementsByTagName('link')[0]
            link1=link.attributes['href'].value
            link2=y.getElementsByTagName('link')[1]
            link3=link2.attributes['href'].value
            embed=discord.Embed(title= f'Title: {title.firstChild.data}', description= f'Published on: {published.firstChild.data}', color = discord.Colour.blue())
            embed.set_author(name=f'{authors}')
            await ctx.send(embed=embed)
            embed=discord.Embed(title='Summary: ', description= f'{summary.firstChild.data}', color = discord.Colour.green())
            embed.add_field(name='Link: ', value=f'{link1}', inline=False)
            embed.add_field(name='Download link: ', value=f'{link3}', inline=False)
            await ctx.send(embed=embed)
            await ctx.send('.................................................................................................................................................')


def setup(client):
    client.add_cog(ArxivAPI(client)) 