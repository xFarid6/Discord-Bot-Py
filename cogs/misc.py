from discord.ext import commands
from typing import Optional, Union, Literal, Annotated
import discord
import aiohttp


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='roll_dice', help='Simulates rolling dice.')
    async def roll(ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))


    @commands.command(name='add')
    async def add(ctx, left: int, right: int):
        await ctx.send(left + right)


    @commands.command(name='99')
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


    @commands.command(name='quote')
    async def quote(ctx):
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
        quote = await get_quote_aio()
        await ctx.send(quote)


    @commands.command()
    async def bottles(ctx, amount: Optional[int] = 99, *, liquid="beer"):
        await ctx.send(f'{amount} bottles of {liquid} on the wall!')


    @commands.command()
    async def shop(ctx, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2], *, item: str):
        await ctx.send(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')


def setup(bot):
    bot.add_cog(MiscCog(bot))
