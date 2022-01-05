# Imports
import discord
import os
from discord.enums import DefaultAvatar
from discord.ext import commands
import json 
from customHelp import help
from dotenv import load_dotenv
import asyncpg 
from asyncpg.pool import create_pool

# Look for a .env file, if found, it will load the environment variables from the file and make them 
# accessible
load_dotenv()

# Load Custom Help Commands
cust_help = help.CustomHelpCommand()

# Managing default and priviledged gateway intents
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Function that checks for prefix for that specific guild from a set of guilds
def get_prefix(client, message):
    with open ("./src/cogs/prefixes.json", "r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]

# Initialise bot instance
client = commands.Bot(command_prefix = None, intents = intents, help_command=cust_help)

# Create database connection pool
db_name = os.environ['DATABASE_NAME']
db_user = os.environ['DATABASE_USER']
db_pass = os.environ['DATABASE_PASSWORD']

async def create_dbpool():
    client.pg_con = await asyncpg.create_pool(database=db_name, user=db_user, password=db_pass)

client.command_prefix = get_prefix

# Error message displayed in discord channel in case invalid command is entered
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Invalid Command!", description = "Command Not Found!",
        color = discord.Color.dark_red())
        await ctx.send(embed = embed)

# Command to load cogs while bot is online
@client.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

# Error message displayed when user triggers `load` command without 
# being granted required permissions
@load.error
async def on_load_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "Missing Permissions!",
        description = "Must have `administrator` permissions to use this command!",
        color = discord.Color.greyple())
        await ctx.send(embed = embed)

# Command to unload cogs when bot is online
@client.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# Error message displayed when user triggers `unload` command without 
# being granted required permissions
@unload.error
async def on_unload_error(ctx, error):
    embed = discord.Embed(title = "Missing Permissions!",
    description = "Must have `administrator` permissions to use this command!",
    color = discord.Color.greyple())
    await ctx.send(embed = embed)

# Command to reload (unload then load) cogs when bot is online. It serves as 
# an efficient way to add/remove/update/fix cogs while bot is actively serving
# its purpose.
@client.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

# Error message displayed when user triggers `reload` command without 
# being granted required permissions
@reload.error
async def on_reload_error(ctx, error):
    embed = discord.Embed(title = "Missing Permissions!",
    description = "Must have `administrator` permissions to use this command!",
    color = discord.Color.greyple())
    await ctx.send(embed = embed)

# Loop that loads cogs when bot is online
for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Connect to Postgres
client.loop.run_until_complete(create_dbpool())

# Code to run the bot
client.run(os.environ['DISCORD_TOKEN'])
