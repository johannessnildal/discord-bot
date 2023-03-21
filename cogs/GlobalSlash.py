import discord
from discord.ext import commands
from discord import app_commands
import datetime

# cog info
# name = "GlobalSlash"
# global slash commands. these are slash commands that are available in every server the bot is in by default.


class GlobalSlash(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @app_commands.command(name = "help", description = "Helpful info and commands") # add if needed: guild = discord.Object(id = 1073336716544450610)) | (this is the test server)
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "Parry", description = "", color = discord.Color.blurple(), timestamp = datetime.datetime.now())
        embed.add_field(name = "Who is Parry?", value = "Parry is a multipurpose bot. It's primarily used to handle moderation tasks to make moderation easier, but also has fun plugins that can be enabled.", inline = False)
        embed.add_field(name = "Dashboard", value = "Everything is controlled through the dashboard. Use */dashboard* to see for yourself!", inline = False)
        embed.add_field(name = "Global Parry commands", value = "`/userinfo` `/serverinfo` `/help` `/dashboard`")
        await interaction.response.send_message(embed = embed, ephemeral = True)
# help command ^


    @app_commands.command(name = "userinfo", description = "Info about any member in the sever") # add if needed: guild = discord.Object(id = 1073336716544450610)) | (this is the test server)
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None:
            member = interaction.user
        roles = [role for role in member.roles]
        embed = discord.Embed(title = "User Information", description = f"Information about user {member.mention}", color = discord.Color.brand_green(), timestamp= datetime.datetime.utcnow())
        embed.set_thumbnail(url = member.avatar)
        embed.add_field(name = "ID", value = member.id, inline=False)
        embed.add_field(name = "Discord name", value = member.name)
        embed.add_field(name = "Server name", value = member.display_name)
        embed.add_field(name = "Status", value = member.status, inline = False)
        embed.add_field(name = "Activity", value = f"{str(member.activity.type).split('.')[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''}")
        embed.add_field(name = "Top role", value = member.top_role.mention)
        embed.add_field(name = f"roles ({len(roles)})", value = " ".join([role.mention for role in roles]), inline = False)
        embed.add_field(name = "Joined at", value = member.joined_at.strftime("%a, %#d %B %Y"), inline = False)
        await interaction.response.send_message(embed = embed, ephemeral = True)
# userinfo command ^


    @app_commands.command(name = "serverinfo", description = "Info about the server") # add if needed: guild = discord.Object(id = 1073336716544450610)) | (this is the test server)
    async def serverinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "Server Information", description = f"Information about server, *{interaction.guild.name}*", color = discord.Color.brand_red(), timestamp= datetime.datetime.utcnow())
        embed.set_thumbnail(url = interaction.guild.icon)
        embed.add_field(name = "ID", value = interaction.guild.id, inline = False)
        embed.add_field(name = "Created on", value = interaction.guild.created_at.strftime("%a, %#d %B %Y"), inline = False)
        embed.add_field(name = "Owner", value = interaction.guild.owner.mention, inline = False)
        embed.add_field(name = "Members", value = interaction.guild.member_count)
        embed.add_field(name = "Channels", value = len(interaction.guild.channels))    
        embed.add_field(name = "Roles", value = len(interaction.guild.roles))
        await interaction.response.send_message(embed = embed, ephemeral = True)
# serverinfo command ^

    @app_commands.command(name = "dashboard", description = "Link to the Parry dashboard") # add if needed: guild = discord.Object(id = 1073336716544450610)) | (this is the test server)
    async def dashboard(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "Dashboard link", description = "Ahoy! Here's ya dashboard!", color = discord.Color.blurple(), timestamp= datetime.datetime.utcnow())
        await interaction.response.send_message(embed = embed, ephemeral = True)
# dashboard command ^


async def setup(client: commands.Bot) -> None:
    await client.add_cog(GlobalSlash(client))
# setup ^