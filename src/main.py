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

# Initialise bot instance
client = commands.Bot(command_prefix = None, intents = intents, help_command=cust_help)

# Create database connection pool
db_name = os.environ['DATABASE_NAME']
db_user = os.environ['DATABASE_USER']
db_pass = os.environ['DATABASE_PASSWORD']

# prefixes_table = "public.prefixes"

async def create_dbpool():
    client.pg_con = await asyncpg.create_pool(database=db_name, user=db_user, password=db_pass)

# Connect to Postgres
client.loop.run_until_complete(create_dbpool())

async def get_prefix(client, message):
    pref_table = os.environ['PREFIXES_TABLE']
    # Check if prefixes table is present, if not, creates one
    await client.pg_con.execute(f"CREATE TABLE IF NOT EXISTS {pref_table}(server_id bigint NOT NULL, server_prefix character varying(5) COLLATE pg_catalog.\"default\" NOT NULL, CONSTRAINT prefixes_pkey PRIMARY KEY (server_id))")

    # If columns are deleted, to re-generate (with constraints)
    await client.pg_con.execute(f"ALTER TABLE IF EXISTS {pref_table} ADD COLUMN IF NOT EXISTS server_id bigint NOT NULL CONSTRAINT prefixes_pkey PRIMARY KEY")

    await client.pg_con.execute(f"ALTER TABLE IF EXISTS {pref_table} ADD COLUMN IF NOT EXISTS server_prefix character varying(5) COLLATE pg_catalog.\"default\" NOT NULL")

    return await client.pg_con.fetchrow(f"SELECT server_prefix FROM {pref_table} WHERE server_id = $1", message.guild.id)

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

# Code to run the bot
client.run(os.environ['DISCORD_TOKEN'])
