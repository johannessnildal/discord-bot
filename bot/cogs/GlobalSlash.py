import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time

bot = discord.Bot()

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(General(bot))
# This is a cog that adds general global slash commands to the bot.
