import discord
from discord.ext import commands
import asyncio
import discord
from discord.ext import commands, tasks
import random
import datetime
from datetime import timedelta

bot = discord.Bot()

cogname = "Parry | Easter Eggs"

class EasterEggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.in_conversation = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "hello there" in message.content.lower():
            await message.channel.send("General Kenobi!")
        elif "i am your father" in message.content.lower():
            await message.channel.send("Noooooo!")

def setup(bot):
    bot.add_cog(EasterEggs(bot))
# This is a cog that adds easter eggs to the bot.