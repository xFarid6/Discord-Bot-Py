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

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, description=description, intents=intents)

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


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(bot.user.id)
    print('------')
    print(f'{bot.user.name} is connected to the following guilds:')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print('------')


@bot.command(name='99')
async def nine_nine(ctx, help='Responds with a random quote from Brooklyn 99'):   
    # A Context holds data such as the channel and guild that the user called the Command from.
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(game=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    print(f'Successfully logged in and booted...!')


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.command(name='add')
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


@bot.command(name='quote')
async def quote(ctx):
    quote = await get_quote_aio()
    await ctx.send(quote)


@bot.command(name='embed')
async def embed(ctx):
    embed = discord.Embed(title='Test', description='This is a test.', color=0xeee657)
    embed.add_field(name='Test', value='Testing.')
    await ctx.send(embed=embed)


@bot.command(name='embed-image')
async def embed_image(ctx):
    embed = discord.Embed(title='Test', description='This is a test.', color=0xeee657)
    embed.set_image(url='https://picsum.photos/200/300/?random')
    await ctx.send(embed=embed)


def to_upper(argument):
    return argument.upper()

@bot.command()
async def up(ctx, *, content: to_upper):
    await ctx.send(content)


class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'{ctx.author} slapped {to_slap} because *{argument}*'


@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)


@bot.command()
async def clean(ctx, *, content: commands.clean_content):
    await ctx.send(content)

# or for fine-tuning

@bot.command()
async def clean(ctx, *, content: commands.clean_content(use_nicknames=False)):
    await ctx.send(content)


class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @classmethod
    async def convert(cls, ctx, argument):
        member = await commands.MemberConverter().convert(ctx, argument)
        return cls(member.joined_at, member.created_at)

    @property
    def delta(self):
        return self.joined - self.created

@bot.command()
async def delta(ctx, *, member: JoinDistance):
    is_new = member.delta.days < 100
    if is_new:
        await ctx.send("Hey you're pretty new!")
    else:
        await ctx.send("Hm you're not so new.")


@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f'{member} joined on {member.joined_at}')


@bot.command()
async def bottles(ctx, amount: Optional[int] = 99, *, liquid="beer"):
    await ctx.send(f'{amount} bottles of {liquid} on the wall!')


@bot.command()
async def shop(ctx, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2], *, item: str):
    await ctx.send(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')


@bot.command()
async def upload(ctx, attachment: Optional[discord.Attachment]):
    if attachment is None:
        await ctx.send('You did not upload anything!')
    else:
        await ctx.send(f'You have uploaded <{attachment.url}>')


@bot.command()
async def upload_many(
    ctx,
    first: discord.Attachment,
    second: Optional[discord.Attachment],
):
    if second is None:
        files = [first.url]
    else:
        files = [first.url, second.url]

    await ctx.send(f'You uploaded: {" ".join(files)}')


@bot.command()
async def wave(to: discord.User = commands.parameter(default=lambda ctx: ctx.author)):
    await ctx.send(f'Hello {to.mention} :wave:')


@bot.command()
async def wave(to: discord.User = commands.Author):
    await ctx.send(f'Hello {to.mention} :wave:')


@bot.command()
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)


@bot.command()
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@bot.command()
@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        'That is a response to a question.',
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',

        'Reply has not been heard yet.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.',
        'My reply is no.',
        'My sources say no.',
        'My reply is no.',
        'My sources say no.',
        'My sources say no.',
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@bot.command()
async def kick(ctx, member: discord.Member, *, reason: str):
    await member.kick(reason=reason)


@bot.command()
@bot.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason: str):
    await member.ban(reason=reason)


"""async def on_message(self, message):
        if message.content.startswith('!deleteme'):
            msg = await message.channel.send('I will delete myself now...')
            await msg.delete()

            # this also works
            await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)

async def on_message_delete(self, message):
    fmt = '{0.author} has deleted the message: {0.content}'
    await message.channel.send(fmt.format(message))
    
    
 async def on_message(self, message):
        if message.content.startswith('!editme'):
            msg = await message.channel.send('10')
            await asyncio.sleep(3.0)
            await msg.edit(content='40')

async def on_message_edit(self, before, after):
    fmt = '**{0.author}** edited their message:\n{0.content} -> {1.content}'
    await before.channel.send(fmt.format(before, after))


 async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)


    self.emoji_to_role = {
                discord.PartialEmoji(name='🔴'): 0, # ID of the role associated with unicode emoji '🔴'.
                discord.PartialEmoji(name='🟡'): 0, # ID of the role associated with unicode emoji '🟡'.
                discord.PartialEmoji(name='green', id=0): 0, # ID of the role associated with a partial emoji's ID.
            }

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        ""Gives a role based on a reaction emoji.""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        ""Removes a role based on a reaction emoji.""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
"""


bot.run(TOKEN, bot=True, reconnect=True)