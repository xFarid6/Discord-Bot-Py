from dotenv.main import load_dotenv
# from discord.ext import commands
import requests
import asyncio
import discord
import random
import json
import os
import aiohttp


# from dotenv import DotEnv
#de = DotEnv()
#de.load_dotenv()


load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')
GUILD = os.getenv('GUILD')

client = discord.Client()


def get_quote():
    """
    It takes a URL, makes a request to that URL, and returns the response as a string
    :return: A string
    """
    url = "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
    # url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = json.loads(response.text)
    # after testing printing out the whole json response
    # quote = data[0]['q'] + " - " + data[0]['a']
    return data["quoteText"]


# rewrite get_quote func using aiohttp
async def get_quote_aio():
    """
    Get the quote from the API and return it as a string.
    :return: A coroutine object.
    """
    url = "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data["quoteText"]


# a function that loads all the commands from the command folder
def load_cogs():
    """
    It loads all the files in the commands folder that end with .py
    """
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            client.load_extension(f'commands.{filename[:-3]}')


# a function that Gives the role "Member" to the user when they join the server
async def member_role(member):
    """
    It gives the "Member" role to the user when they join the server
    """
    role = discord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(role)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        # if guild.name == GUILD:
        #   break
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )
    

        for channel in guild.channels:
           print(f'{channel.name}(id: {channel.id})')

    # simplify the for loop above
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX + "hello"):
        await message.channel.send('Hello!')
        
    # if the message starts with &quote, get a quote and send it
    if message.content.startswith(PREFIX + "quote"):
        quote = await get_quote_aio()
        await message.channel.send(quote)

    # if the message starts with &roll, roll a dice and send the result
    if message.content.startswith(PREFIX + "roll"):
        await message.channel.send(str(random.randint(1, 6)))

    # if the content starts with &help, execute the help.py file in the commands folder
    if message.content.startswith(PREFIX + "help"):
        await message.channel.send("""
        **Commands:**
        **&hello** - Says hello
        **&quote** - Gets a quote
        **&roll** - Rolls a dice
        **&help** - Shows this message
        """)

    # check if the message starts with the prefix and if it is the case execute the command
    if message.content.startswith(PREFIX):
        command = message.content.split(" ")[0][len(PREFIX):]
        args = message.content.split(" ")[1:]
        print(f"{command} {args}")
        if command in commands:
            await commands[command](message, args)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)
