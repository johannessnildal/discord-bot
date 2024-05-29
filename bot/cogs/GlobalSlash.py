import discord
from discord.ext import commands

bot = discord.Bot()

class GlobalSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.tree.add_command(self.app)

    @bot.slash_command(name = "help", description = "Helpful info and commands")
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(title = "Parry", description = "", color = discord.Color.blurple())
        embed.add_field(name = "Who is Parry?", value = "Parry is a multipurpose bot. It's primarily used to handle moderation tasks to make moderation easier, but also has fun plugins that can be enabled.", inline = False)
        embed.add_field(name = "Dashboard", value = "Everything is controlled through the dashboard. Use */dashboard* to see for yourself!", inline = False)
        embed.add_field(name = "Global Parry commands", value = "`/userinfo` `/serverinfo` `/help` `/dashboard`")
        await interaction.response.send_message(embed = embed, ephemeral = True)
        # help command ^

    async def cog_load(self):
        self.bot.tree.add_command(self.app)
        await self.bot.tree.sync()

    async def cog_unload(self):
        self.bot.tree.remove_command(self.app)
        await self.bot.tree.sync()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GlobalSlash(bot))
