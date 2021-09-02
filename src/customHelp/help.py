# imports
import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()


    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Commands", description="All commands of the bot", 
        color=discord.Color.dark_green())
        for cog in mapping:
            if cog!=None:
                command_str = ""
                for i in [command.name for command in mapping[cog]]:
                    command_str += "`" + str(i) + "`" + "\n"
                embed.add_field(name=f'{cog.qualified_name}', value=f'{command_str}')
            else:
                pass
            
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
     
        embed = discord.Embed(title=f'{cog.qualified_name}', 
        description = "None", color=discord.Color.greyple())
        for command in cog.get_commands():
            help_text = command.help.split('\n')[1]
            embed.add_field(name=f'{command.name}', value=f'{help_text}', inline=False)
        await self.get_destination().send(embed=embed)
        

    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

    async def send_command_help(self, command):
        if (len(command.aliases)==0):
            aliases = str(command.name)
        else:

            aliases=''
            for i in command.aliases:
                aliases += str(i)+', '
            aliases = aliases[:-2:]
        embed = discord.Embed(title = f'{command.name}',
        description = f'{command.help}', color = discord.Color.red())
        embed.add_field(name ="Aliases" , value = f'{aliases}' )
        await self.get_destination().send(embed = embed)
    #self.client(help_command=commands.MinimalHelpCommand())



def setup(client):
    client.add_cog(CustomHelpCommand(client))