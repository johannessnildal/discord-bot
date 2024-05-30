import discord
from discord.ext import commands

bot = discord.Bot()

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency is **{round(self.bot.latency * 1000)}ms**")
    # ping command ^

    @commands.slash_command(title="Userinfo", description="Get information about a user")
    async def userinfo(self, ctx, user: discord.Member):
        embed = discord.Embed(title="Userinfo", description=f"Here is information about {user}", color=discord.Color.green(), timestamp=discord.utils.utcnow())
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Name", value=f"Username: {user.name} | Display: {user.display_name}", inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined server", value=user.joined_at.strftime("%d-%m-%y %H:%M"))
        embed.add_field(name="Account created", value=user.created_at.strftime("%d-%m-%y %H:%M"))
        role = ', '.join(role.name for role in user.roles if role.name != user.name)
        message_count = len(await ctx.channel.history().flatten())
        embed.add_field(name="Role(s)", value=role, inline=False)
        embed.add_field(name="Messages sent", value=message_count, inline=False)
        embed.set_footer(text="Parry | Userinfo")
        if user.bot:
            embed.add_field(name="This is a bot/application account.", value="", inline=False)
        await ctx.respond(embed=embed)
    # userinfo command ^

def setup(bot):
    bot.add_cog(Info(bot))
# This is a cog that adds info commands to the bot.