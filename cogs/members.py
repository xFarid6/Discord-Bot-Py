import discord
from discord.ext import commands


class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')


    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')


    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.


    @commands.command(name='embed')
    async def embed(ctx):
        embed = discord.Embed(title='Test', description='This is a test.', color=0xeee657)
        embed.add_field(name='Test', value='Testing.')
        await ctx.send(embed=embed)


    @commands.command(name='embed-image')
    async def embed_image(ctx):
        embed = discord.Embed(title='Test', description='This is a test.', color=0xeee657)
        embed.set_image(url='https://picsum.photos/200/300/?random')
        await ctx.send(embed=embed)
        

    def to_upper(argument):
        return argument.upper()

    @commands.command()
    async def up(ctx, *, content: to_upper):
        await ctx.send(content)


    @commands.command()
    async def wave(to: discord.User):
        await ctx.send(f'Hello {to.mention} :wave:')


    @commands.command()
    async def joined(ctx, *, member: discord.Member):
        await ctx.send(f'{member} joined on {member.joined_at}')
    

    @commands.group()
    async def cool(ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


    @commands.command()
    async def report(ctx, *, member: discord.Member, reason: str):
        """Reports a user"""
        await ctx.send(f'{member} has been reported for {reason}')
        

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MembersCog(bot))
