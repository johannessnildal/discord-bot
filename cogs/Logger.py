import discord
from discord.ext import commands
import json
from datetime import datetime

# cog info
# name = "Logger"
# audit logger that track user events.

# to-do: support for MainModeration cog so that it can log MainModeration commands and add exceptions for commands that are not logged.


with open('config.json', 'r') as f:
    data = json.load(f)
    PREFIX = data["PREFIX"]
    CHANNEL_ID = data["LOGGER_CHANNEL_ID"]


class Logger(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = CHANNEL_ID
        guild = member.guild
        channel = guild.get_channel(channel_id)
        message = f"{member} has joined the server."
        await channel.send(message)
    # member join ^

    @commands.Cog.listener()
    async def leave(self, member):
        channel_id = CHANNEL_ID
        guild = member.guild
        channel = guild.get_channel(channel_id)
        embed = discord.Embed(title="Member Left", color=discord.Color.red())
        embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar.url)
        embed.set_footer(text=f"Member ID: {member.id} | Left at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        await channel.send(embed=embed)
    # member leave ^

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if before.author.bot:
                return
            channel_id = CHANNEL_ID
            channel = self.client.get_channel(channel_id)
            embed = discord.Embed(title="Message Edited", color=discord.Color.gold(), timestamp=datetime.now())
            embed.set_author(name=f"{before.author.name}#{before.author.discriminator}", icon_url=before.author.avatar.url)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.set_footer(text=f"Channel: #{before.channel.name}")
            await channel.send(embed=embed)
        except AttributeError or TypeError:
            pass
    # message edit ^

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            channel_id = CHANNEL_ID
            guild = message.guild
            channel = guild.get_channel(channel_id)
            embed = discord.Embed(title="Message deleted",
                                description=f"**User:** {message.author.mention}\n**Channel:** {message.channel.mention}",
                                color=discord.Color.red(),
                                timestamp=datetime.now())
            if message.author is not None:
                embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
            else:
                embed.set_author(name="Unknown", icon_url=self.client.user.default_avatar.url)
            embed.add_field(name="Message content", value=message.content or "*empty*")
            await channel.send(embed=embed)
        except AttributeError:
            pass
    # message delete ^


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Logger(client))
# setup ^