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


"""
https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#invocation-context

Context.guild returns the Guild of the command, if any.

Context.message returns the Message of the command.

Context.author returns the Member or User that called the command.

Context.send() to send a message to the channel the command was used in.
"""

initial_extensions = ['cogs.actions',
                      'cogs.admin',
                      'cogs.general',
                      'cogs.members',
                      'cogs.misc',
                      'cogs.owner',
                      'cogs.slapper',]

bot = commands.Bot(command_prefix=PREFIX, description=description) # intents=intents
# print(dir(bot))
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

    # Setting `Playing ` status
    await bot.change_presence(activity=discord.Game(name="a game"))

    # Setting `Streaming ` status
    #  bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))

    # Setting `Listening ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

    # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    # await bot.change_presence(game=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    # print(f'Successfully logged in and booted...!')


async def on_message(self, message):
    # we do not want the bot to reply to itself
    if message.author.id == self.user.id:
        return

    if message.content.startswith('!hello'):
        await message.reply('Hello!', mention_author=True)
        
    if message.content.startswith('!p'):
        # if message.channel.id != 966316388924932217:
        if message.channel.name == 'musica-qua-plz':
            await message.channel.send('https://www.youtube.com/watch?v=i5-0F5E-mqc')

    if message.content.startswith('!deleteme'):
        msg = await message.channel.send('I will delete myself now...')
        await msg.delete()

        # this also works
        await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)

    if message.content.startswith('!editme'):
        msg = await message.channel.send('10')
        await asyncio.sleep(3.0)
        await msg.edit(content='40')


@bot.event
async def on_message_edit(self, before, after):
    fmt = '**{0.author}** edited their message:\n{0.content} -> {1.content}'
    await before.channel.send(fmt.format(before, after))


@bot.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)


@bot.event
async def on_message_delete(self, message):
    fmt = '{0.author} has deleted the message: {0.content}'
    await message.channel.send(fmt.format(message))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(TOKEN) # bot=True, reconnect=True