from discord.ext import commands
import discord
from typing import Optional, Union, Literal, Annotated


class ActionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def clean(ctx, *, content: commands.clean_content(use_nicknames=False)):
        await ctx.send(content)


    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))


    @commands.command()
    async def repeat(ctx, times: int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await ctx.send(content)


    @commands.command()
    async def echo(ctx, *, message: str):
        await ctx.send(message)


    @commands.command()
    async def upload(ctx, attachment: Optional[discord.Attachment]):
        if attachment is None:
            await ctx.send('You did not upload anything!')
        else:
            await ctx.send(f'You have uploaded <{attachment.url}>')


    @commands.command()
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


    @commands.command(aliases=['8ball', 'eight_ball', 'eightball', '8b'])
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


def setup(bot):
    bot.add_cog(ActionsCog(bot))
