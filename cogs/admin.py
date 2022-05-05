from discord.ext import commands
import discord
import asyncio
import aiohttp
import json
import os
import sys
import time
import datetime
import random
import re
import traceback


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
        