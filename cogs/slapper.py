from discord.ext import commands
import discord


class SlapperFormat(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'{ctx.author} slapped {to_slap} because *{argument}*'




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

    
class Slapper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slap(ctx, *, reason: SlapperFormat):
        await ctx.send(reason)

    
    @commands.command()
    async def delta(ctx, *, member: JoinDistance):
        is_new = member.delta.days < 100
        if is_new:
            await ctx.send("Hey you're pretty new!")
        else:
            await ctx.send("Hm you're not so new.")


def setup(bot):
    bot.add_cog(Slapper(bot))
