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

intents = discord.Intents.default().all()
intents.members = True


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


@bot.listen()
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(bot.user.id)
    print('------')
    print(f'{bot.user.name} is connected to the following guilds:')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print('------')

    # Setting `Playing ` status
    await bot.change_presence(activity=discord.Game(name="pygame, discord-py"))

    # Setting `Streaming ` status
    #  bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))

    # Setting `Listening ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

    # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    # await bot.change_presence(game=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    # print(f'Successfully logged in and booted...!')


@bot.listen()
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author.id == bot.user.id: return
    if message.author.bot: return

    if message.content.startswith(PREFIX + 'hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith(PREFIX + 'deleteme'):
        await message.delete()

    # if message.content.startswith(PREFIX + 'editme'): # cannot edit other's messages, dummy
        # await message.edit(content='Edited!')
    if message.content == PREFIX + 'lenny':
        await message.delete()
        await message.channel.send('( ͡° ͜ʖ ͡°)')

    if message.content.startswith(PREFIX + 'reactme'):
        await message.add_reaction('👍')

    # if a message starting with !p is sent outside the musica-qua-plz channel, delete the message
    if message.content.startswith('!p') and message.channel.name != 'musica-qua-plz':
        # find the last message sent by L'erede della musica
        await asyncio.sleep(10)
        # last_message = await message.channel.history(limit=1).flatten()

        await message.channel.send('!leave')
        await asyncio.sleep(3)

        await message.channel.send('!p https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        await message.channel.send('Dovresti mettere la musica dal canale apposta.\n Altrimenti vieni Rickrollato!')
        await message.channel.send('!skip')


@bot.listen()
async def on_message_edit(before, after):
    fmt = '**{0.author}** edited their message:\n{0.content} -> {1.content}'
    await before.channel.send(fmt.format(before, after))


@bot.listen()
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)


@bot.listen()
async def on_message_delete(message):
    fmt = '{0.author} has deleted the message: {0.content}'
    await message.channel.send(fmt.format(message))


@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(TOKEN) # bot=True, reconnect=True
