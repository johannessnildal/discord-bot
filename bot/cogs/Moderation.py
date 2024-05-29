import discord
from discord.ext import commands
import asyncio
from discord.ui import Button, View

bot = discord.Bot()

class DeleteToggleView(View):
    def __init__(self, timeout=20):
        super().__init__(timeout=timeout)
        self.delete_toggle = True

    @discord.ui.button(label="Keep message", style=discord.ButtonStyle.gray, emoji="🔒")
    async def toggle_delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.delete_toggle = False
        button.disabled = True
        button.style = discord.ButtonStyle.green
        button.label = "Message kept"
        button.emoji = "✅"
        await interaction.response.edit_message(view=self)

cogname = "Parry | Moderation"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int,):
        if amount > 100:
            await ctx.send("You can't delete more than 100 messages at once!")
            return
        elif amount < 1:
            await ctx.send("You have to delete at least one message!")
            return
        await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(title="Clear", description=f"Deleted **{amount}** messages!", color=discord.Color.brand_red(), timestamp=ctx.message.created_at)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        embed.add_field(name="" , value="####", inline=False)
        embed.set_footer(text=cogname)
                
        view = DeleteToggleView()
        clearmsg = await ctx.send(embed=embed, view=view)
            
        for i in range(20, 0, -1):
            if not view.delete_toggle:
                # Remove the countdown field
                embed.set_field_at(2, name="Self-Delete disabled", value="", inline=False)
                await clearmsg.edit(embed=embed)
                break
            embed.set_field_at(2, name="Self-Delete", value=f"This message will delete itself in {i}s", inline=False)
            await clearmsg.edit(embed=embed)
            await asyncio.sleep(1)
                
        if view.delete_toggle:
            await clearmsg.delete()
# clear command ^

def setup(bot):
    bot.add_cog(Moderation(bot))
# This is a cog that adds moderation commands to the bot.

