from discord.ext import commands
import discord


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_url = "https://github.com/xFarid6/Discord-Bot-Py"
        self.support_url = "https://github.com/xFarid6/Discord-Bot-Py/issues"
        self.invite_url = "https://discordapp.com/api/oauth2/authorize?client_id=723990989841003520&permissions=8&scope=bot"


    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


    @commands.command()
    async def invite(self, ctx):
        """Invite the bot to your server!"""
        await ctx.send(f'Invite the bot to your server: {self.invite_url}')


    @commands.command()
    async def support(self, ctx):
        """Get support for the bot!"""
        await ctx.send(f'Get support for the bot: {self.support_url}')
        

    @commands.command()
    async def github(self, ctx):
        """Get the bot's github!"""
        await ctx.send(f'Get the bot\'s github: {self.github_url}')


    @commands.command(name='coolbot')
    async def cool_bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('This bot is cool. :)')


    @commands.command()
    async def test(ctx, *args):
        arguments = ', '.join(args)
        await ctx.send(f'{len(args)} arguments: {arguments}')
        

    @commands.command(name='bot')
    async def _bot(ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')


def setup(bot):
    bot.add_cog(GeneralCog(bot))
