import discord
from discord.ext import commands
import os
from discord.commands import Option

bot = discord.Bot()
prefix = os.getenv("PREFIX")

general_color = discord.Color.blue()
info_color = discord.Color.brand_green()
moderation_color = discord.Color.brand_red()
admin_color = discord.Color.from_rgb(0,0,0)
error_color = discord.Color.orange()

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="I've got your back! Get a list of commands or details about a specific command")
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
            elif command == "lock":
                embed = discord.Embed(
                    title=f"/lock | admin",
                    description="Lock the current channel, preventing users from sending messages.",
                    color=admin_color
                )
                embed.add_field(name="Usage", value=f"`/lock`", inline=False)
            elif command == "unlock":
                embed = discord.Embed(
                    title=f"/unlock | admin",
                    description="Unlock the current channel, allowing users to send messages again.",
                    color=admin_color
                )
                embed.add_field(name="Usage", value=f"`/unlock`", inline=False)
            else:
                embed = discord.Embed(
                    title="⚠️ Error",
                    description=f"Sorry matey! One of two things happened: Either there is no command named `{command}`, or i've just been too lazy to add further information regarding `{command}`. I'm a parrot, give me a break!😔",
                    color=error_color
                )
                embed.set_footer(text="Parry | Errors")
        else:
            embed = discord.Embed(
                title="🦜 Help",
                description="Here is a list of available commands:",
                color=discord.Color.from_rgb(117,201,177)
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(name="Important", value="`.` are prefix commands, `/` are app commands, `[]` are message commands (message commands are accessed by right clicking a message -> apps)", inline=False)
            embed.add_field(name="General", value="`/help` `/link`", inline=False)
            embed.add_field(name="Further help", value="By saying 'hello parry' in chat (without prefix), you unlock a set of helpful info you can ask for. Like:\n`prefix` `ping` `link`", inline=False)
            embed.add_field(name="Info", value=f"`/userinfo` `/serverinfo`", inline=False)
            embed.add_field(name="Moderation", value=f"`{prefix}clear` `/log_channel` `[]log_message`", inline=False)
            embed.add_field(name="Admin", value="`/lock` `/unlock`", inline=False)
            embed.add_field(name="🤐 Psst!", value="Parry is a bird of many secrets. Find out if you can!", inline=False)
            embed.set_footer(text="Use `/help <command>` to get detailed information about a specific command.")
        await ctx.respond(embed=embed)
    # help command ^

def setup(bot):
    bot.add_cog(General(bot))
# This is a cog that adds general useful commands to the bot.
