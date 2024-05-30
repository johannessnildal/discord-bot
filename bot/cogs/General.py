import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from discord.commands import Option

bot = discord.Bot()
prefix = os.getenv("PREFIX")

general_color = discord.Color.blue()
moderation_color = discord.Color.brand_red()
info_color = discord.Color.brand_green()
error_color = discord.Color.orange()

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Get a list of commands or details about a specific command")
    async def help(self, ctx, command: Option(str, "Enter a command to get specific information", required=False)): # type: ignore
        if command:
            command = command.lower()
            if command == "userinfo":
                embed = discord.Embed(
                    title="/userinfo | info",
                    description="Usage: `/userinfo @user`\nGet information about a specified user.",
                    color=info_color
                )
            elif command == "clear":
                embed = discord.Embed(
                    title=f"{prefix}clear | moderation",
                    description=f"Usage: `{prefix}clear all`\n`{prefix}clear <amount>`\nDelete a specified amount of messages in the current channel. oooh, spooky!",
                    color=moderation_color
                )
            elif command == "link":
                embed = discord.Embed(
                    title="/link | general",
                    description="Usage: `/link`\nGet a link to invite me to your server! Who wouldn't want a screeching parrot in their server?",
                    color=general_color
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Error",
                    description=f"Sorry matey! One of two things happened: Either there is no command named `{command}`, or i've just been too lazy to add further information regarding `{command}`. I'm a parrot, give me a break!😔",
                    color=error_color
                )
        else:
            embed = discord.Embed(
                title="Help",
                description="Here is a list of available commands:",
                color=general_color
            )
            embed.add_field(name="General", value="`/help` | `/link`", inline=False)
            embed.add_field(name="Moderation", value=f"`{prefix}clear`", inline=False)
            embed.add_field(name="Info", value=f"`/userinfo` | `{prefix}ping`", inline=False)
            embed.set_footer(text="Use `/help <command>` to get detailed information about a specific command.")
        await ctx.respond(embed=embed)
    # help command ^

    @commands.slash_command(title="Invite", description="Get a link to invite Parry to your server.")
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite", description="Ayee! Here's an invite for me:", color=discord.Color.blue(), timestamp=discord.utils.utcnow())
        embed.add_field(name="", value="[Copy or click here!](https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands)")
        embed.set_footer(text="Parry | Invite")
        await ctx.respond(embed=embed)
    # invite command ^

def setup(bot):
    bot.add_cog(General(bot))
# This is a cog that adds general useful commands to the bot.
