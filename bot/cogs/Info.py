import discord
from discord.ext import commands

bot = discord.Bot()

cogname = "Parry | Info"

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency is **{round(self.bot.latency * 1000)}ms**")
    # ping command ^

    @commands.slash_command(title="Userinfo", description="Get information about a user")
    async def userinfo(self, ctx, user: discord.Member):
        embed = discord.Embed(title="User info", description=f"Here is some juicy gossip about {user} 😄", color=discord.Color.green(), timestamp=discord.utils.utcnow())
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Name", value=f"Username: {user.name} | Display: {user.display_name}", inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined server", value=user.joined_at.strftime("%d-%m-%y %H:%M"))
        embed.add_field(name="Account created", value=user.created_at.strftime("%d-%m-%y %H:%M"))
        role = ', '.join(role.name for role in user.roles if role.name != user.name)
        message_count = len(await ctx.channel.history().flatten())
        embed.add_field(name="Role(s)", value=role, inline=False)
        embed.add_field(name="Messages sent", value=message_count, inline=False)
        embed.set_footer(text=cogname)
        if user.bot:
            embed.add_field(name="This is a bot/application account.", value="", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)
    # userinfo command ^

    @commands.slash_command(title="Serverinfo", description="Get information about the server")
    @commands.has_guild_permissions(manage_guild=True)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="Server info", description=f"Here is some juicy gossip about {guild} 🦜", color=discord.Color.green(), timestamp=discord.utils.utcnow())
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name="Name", value=guild.name, inline=False)
        embed.add_field(name="ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=False)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Channels", value=len(guild.channels), inline=False)
        embed.add_field(name="Verification level", value=guild.verification_level, inline=False)
        embed.add_field(name="Created at", value=guild.created_at.strftime("%d-%m-%y %H:%M"), inline=False)
        embed.set_footer(text=cogname)
        await ctx.respond(embed=embed, ephemeral=True)
    # serverinfo command ^

def setup(bot):
    bot.add_cog(Info(bot))
# This is a cog that adds info commands to the bot.