import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

bot = discord.Bot()
prefix = os.getenv("PREFIX")

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(title="Help", description="Get a list of commands")
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="Here is a list of commands", color=discord.Color.brand_red(), timestamp=discord.utils.utcnow())
        embed.add_field(name="Prefix", value=f"`{prefix}`")
        embed.add_field(name="General", value=f"`/help`", inline=False)
        embed.add_field(name="Moderation", value=f"`{prefix}clear` | `/kick` | `/ban`", inline=False)
        embed.add_field(name="Info/Stats", value=f"`{prefix}ping` | `/userinfo`", inline=False)
        embed.set_footer(text="Parry | Help")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
# This is a cog that adds general useful commands to the bot.
