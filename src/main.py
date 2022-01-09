# Imports
import discord
import os
from discord.enums import DefaultAvatar
from discord.ext import commands
from customHelp import help
from dotenv import load_dotenv
import asyncpg 

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

# Loop that loads cogs when bot is online
for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Code to run the bot
client.run(os.environ['DISCORD_TOKEN'])
