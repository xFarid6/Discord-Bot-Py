from discord.ext import commands
import discord


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def invite(self, ctx):
        """Invite the bot to your server!"""
        await ctx.send(f'Invite the bot to your server: {self.bot.invite_url}')

    @commands.command()
    async def support(self, ctx):
        """Get support for the bot!"""
        await ctx.send(f'Get support for the bot: {self.bot.support_url}')
        
    @commands.command()
    async def github(self, ctx):
        """Get the bot's github!"""
        await ctx.send(f'Get the bot\'s github: {self.bot.github_url}')
        

def setup(bot):
    bot.add_cog(GeneralCog(bot))
