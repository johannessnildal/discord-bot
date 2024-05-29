import discord
from discord.ext import commands

bot = discord.Bot()

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(title="Ping", description="Check the bot's latency")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms")
        # ping command ^

def setup(bot):
    bot.add_cog(Global(bot))
# This is a cog that adds general useful commands to the bot.
