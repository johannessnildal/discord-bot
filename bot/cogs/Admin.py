import discord
from discord.ext import commands
import discord
from discord.ext import commands
from datetime import datetime

bot = discord.Bot()

cogname = "Parry | Admin"
locked = discord.Color.from_rgb(0,0,0) # Black
unlocked = discord.Color.from_rgb(255,255,255) # White

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="lock",
        description="Lock a specified channel"
    )
    async def lock_channel(self, ctx, channel: discord.Option(discord.TextChannel, "Select a channel to lock")): # type: ignore
        guild = ctx.guild
        overwrite = discord.PermissionOverwrite(send_messages=False)
        
        # Check current permissions of the @everyone role in the specified channel
        current_overwrites = channel.overwrites_for(guild.default_role)
        
        # If the channel is already locked, send an ephemeral error message
        if current_overwrites.send_messages is False:
            error_embed = discord.Embed(
                title="❗️ Channel Already Locked",
                description=f"Channel {channel.mention} is already locked.\nThis message will be deleted shortly.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await ctx.respond(embed=error_embed, ephemeral=True, delete_after=15)
            return
        
        # Lock the channel by denying the send_messages permission
        await channel.set_permissions(guild.default_role, overwrite=overwrite)

        # Create embed for confirmation to the user
        confirmation_embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"Channel {channel.mention} has been locked.",
            color=locked,
            timestamp=datetime.now()
        )
        confirmation_embed.set_footer(text=cogname)
        await ctx.respond(embed=confirmation_embed, delete_after=10)

        # Create embed for notification in the locked channel
        notification_embed = discord.Embed(
            title="🔒 Locked Channel",
            description="This channel has been locked by an admin. You cannot send messages here.",
            color=locked,
            timestamp=datetime.now()
        )
        notification_embed.add_field(name="Locked by", value=ctx.author.mention, inline=False)
        notification_embed.set_footer(text=cogname)
        await channel.send(embed=notification_embed)
    # lock command ^

    @commands.slash_command(
        name="unlock",
        description="Unlock a specified channel"
    )
    async def unlock_channel(self, ctx, channel: discord.Option(discord.TextChannel, "Select a channel to unlock")): # type: ignore
        guild = ctx.guild
        overwrite = discord.PermissionOverwrite(send_messages=None)

        # Check current permissions of the @everyone role in the specified channel
        current_overwrites = channel.overwrites_for(guild.default_role)

        # If the channel is already unlocked, send an ephemeral error message
        if current_overwrites.send_messages is None:
            error_embed = discord.Embed(
                title="❗️ Channel Already Unlocked",
                description=f"Channel {channel.mention} is already unlocked.\nThis message will be deleted shortly.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await ctx.respond(embed=error_embed, ephemeral=True, delete_after=15)
            return

        # Unlock the channel by allowing the send_messages permission
        await channel.set_permissions(guild.default_role, overwrite=overwrite)

        # Create embed for confirmation to the user
        confirmation_embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"Channel {channel.mention} has been unlocked.",
            color=unlocked,
            timestamp=datetime.now()
        )
        confirmation_embed.set_footer(text=cogname)
        await ctx.respond(embed=confirmation_embed, delete_after=10)

        # Create embed for notification in the unlocked channel
        notification_embed = discord.Embed(
            title="🔓 Unlocked Channel",
            description="This channel has been unlocked by an admin. You can now send messages here.",
            color=unlocked,
            timestamp=datetime.now()
        )
        notification_embed.add_field(name="Unlocked by", value=ctx.author.mention, inline=False)
        notification_embed.set_footer(text=cogname)
        await channel.send(embed=notification_embed)
    # unlock command ^

def setup(bot):
    bot.add_cog(Admin(bot))
# This is a cog that adds admin (high-level) commands to the bot.