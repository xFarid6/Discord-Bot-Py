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


    @commands.command(name='delete-channel')
    @commands.has_role('admin')
    async def delete_channel(ctx, channel_name='real-python'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            print(f'Deleting channel: {channel_name}')
            await existing_channel.delete()


    @commands.command(name='create-role')
    @commands.has_role('admin')
    async def create_role(ctx, role_name='real-python'):
        guild = ctx.guild
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if not existing_role:
            print(f'Creating a new role: {role_name}')
            await guild.create_role(name=role_name)


    @commands.command()
    async def purge(ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    
    @commands.command()
    async def kick(ctx, member: discord.Member, *, reason: str):
        await member.kick(reason=reason)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(ctx, member: discord.Member, *, reason: str):
        await member.ban(reason=reason)
        

def setup(bot):
    bot.add_cog(AdminCog(bot))
