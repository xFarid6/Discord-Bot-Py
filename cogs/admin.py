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


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

def setup(bot):
    bot.add_cog(AdminCog(bot))