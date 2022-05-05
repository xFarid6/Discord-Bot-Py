from dotenv.main import load_dotenv

# from dotenv import DotEnv
#de = DotEnv()
#de.load_dotenv()


load_dotenv()


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
