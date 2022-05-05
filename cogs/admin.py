from discord.ext import commands
import discord
import asyncio
import aiohttp
import json
import os
import sys
import random


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    

    @commands.command(name='create-channel')
    @commands.has_role('admin')
    async def create_channel(ctx, channel_name='real-python'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)

def setup(bot):
    bot.add_cog(AdminCog(bot))
