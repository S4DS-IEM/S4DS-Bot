import discord
import os
from discord.ext import commands

intents=discord.Intents.default()
intents.members=True

client=commands.Bot(command_prefix='-',intents=intents)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

f=open("token.txt","r")
token = f.read()
f.close()

client.run(token)
