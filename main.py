from dotenv.main import load_dotenv
from discord.ext import commands, tasks
import requests
import asyncio
import discord
import random
import json
import os
import aiohttp
from typing import Optional, Union, Literal, Annotated


# from dotenv import DotEnv
#de = DotEnv()
#de.load_dotenv()


load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')
GUILD = os.getenv('GUILD')


description = '''
An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

# intents = discord.Intents.default()
# intents.members = True

bot = commands.Bot(command_prefix=PREFIX, description=description) # intents=intents

"""
https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#invocation-context

Context.guild returns the Guild of the command, if any.

Context.message returns the Message of the command.

Context.author returns the Member or User that called the command.

Context.send() to send a message to the channel the command was used in.
"""

initial_extensions = ['cogs.admin',
                      'cogs.members',
                      'cogs.general',
                      'cogs.owner',]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(bot.user.id)
    print('------')
    print(f'{bot.user.name} is connected to the following guilds:')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print('------')

bot.run(TOKEN) # bot=True, reconnect=True