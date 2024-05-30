import discord
from discord.ext import commands
import os
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
                    description="Get information about a specified user.",
                    color=info_color
                )
                embed.add_field(name="Usage", value="`/userinfo @user`", inline=False)
            elif command == "serverinfo":
                embed = discord.Embed(
                    title="/serverinfo | info",
                    description="Get information about the current server.",
                    color=info_color
                )
                embed.add_field(name="Usage", value="`/serverinfo`", inline=False)
            elif command == "clear":
                embed = discord.Embed(
                    title=f"{prefix}clear | moderation",
                    description="Delete a specified amount of messages in the current channel. oooh, spooky!",
                    color=moderation_color
                )
                embed.add_field(name="🚧 AYEE!", value="Be careful: This command can have serious, permanent consequences.", inline=False)
                embed.add_field(name="Usage", value=f"`{prefix}clear <amount>`\n`{prefix}clear all`", inline=False)
            elif command == "log_channel":
                embed = discord.Embed(
                    title=f"{prefix}log_channel | moderation",
                    description="Set a channel to log moderation actions in. You can also use this command to disable logging by providing `disable` as the channel.",
                    color=moderation_color
                )
                embed.add_field(name="Usage", value=f"`{prefix}log_channel #channel`", inline=False)
            elif command == "log_message":
                embed = discord.Embed(
                    title="log_message | moderation",
                    description="Log a message to the moderation log. This command is accessed by right clicking a message and selecting 'Apps'.",
                    color=moderation_color
                )
            elif command == "ping":
                embed = discord.Embed(
                    title=f"{prefix}ping | info",
                    description="Get the latency of the bot in milliseconds.",
                    color=info_color
                )
                embed.add_field(name="Usage", value=f"`{prefix}ping`", inline=False)
            elif command == "link":
                embed = discord.Embed(
                    title="/link | general",
                    description="Get a link to invite me to your server! Who wouldn't want a screeching parrot in their server?",
                    color=general_color
                )
                embed.add_field(name="Usage", value="`/link`", inline=False)
            else:
                embed = discord.Embed(
                    title="⚠️ Error",
                    description=f"Sorry matey! One of two things happened: Either there is no command named `{command}`, or i've just been too lazy to add further information regarding `{command}`. I'm a parrot, give me a break!😔\nThis message will be deleted shortly.",
                    color=error_color,
                    delete_after=15,
                    timestamp=ctx.message.created_at
                )
                embed.set_footer(text="Parry | Errors")
        else:
            embed = discord.Embed(
                title="Help",
                description="Here is a list of available commands:",
                color=general_color
            )
            embed.add_field(name="Important", value="`.` are prefix commands, `/` are app commands, `[]` are message commands (message commands are accessed by right clicking a message -> apps)", inline=False)
            embed.add_field(name="General", value="`/help` | `/link`", inline=False)
            embed.add_field(name="Moderation", value=f"`{prefix}clear` | `/log_channel` | `[]log_message`", inline=False)
            embed.add_field(name="Info", value=f"`/userinfo` | `/serverinfo` | `{prefix}ping`", inline=False)
            embed.set_footer(text="Use `/help <command>` to get detailed information about a specific command.")
        await ctx.respond(embed=embed)
    # help command ^

    @commands.slash_command(title="Invite", description="Get a link to invite Parry to your server.")
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite", 
            description="Ayee! Here's an invite for me:", 
            color=discord.Color.blue(), 
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="", value="[Copy or click here!](https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands)")
        embed.set_footer(text="Parry | Invite")
        await ctx.respond(embed=embed)
    # invite command ^

def setup(bot):
    bot.add_cog(General(bot))
# This is a cog that adds general useful commands to the bot.
