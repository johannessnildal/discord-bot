import discord
from discord.ext import commands
import asyncio
from discord.ui import Button, View
from typing import Union

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
    async def clear(self, ctx, amount: Union[int, str]):
        if amount == "all":
            await ctx.channel.purge()
            embed = discord.Embed(title="Clear", description="All messages cleared!", color=discord.Color.brand_red(), timestamp=ctx.message.created_at)
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
        else:
            try:
                amount = int(amount)
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
            except ValueError:
                embed = discord.Embed(title="⚠️ Error", description="Invalid amount parameter. Please provide a number or 'all'.", color=discord.Color.orange())
                embed.add_field(name="Examples", value=f"`{ctx.prefix}clear 5`\n`{ctx.prefix}clear all`")
                embed.set_footer(text=cogname)
                await ctx.send(embed=embed)
    # clear command ^

    @commands.message_command(name="Log Message")
    @commands.has_permissions(administrator=True)
    async def log_message(self, ctx: commands.Context, message: discord.Message):
        embed = discord.Embed(title="👀 Logged Message", description=message.content, color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
        embed.timestamp = message.created_at
        embed.add_field(name="Message ID", value=message.id)
        embed.add_field(name="Channel", value=message.channel.mention)
        embed.add_field(name="Jump to message", value=f"[Click here]({message.jump_url})", inline=False)
        embed.set_footer(text=f"Logged by {ctx.author.display_name}")
        await ctx.send(embed=embed)

        embed2 = discord.Embed(title="Message Logged", description=f"Message by {message.author.display_name} in {message.channel.mention} has been logged!", color=discord.Color.brand_red())
        await ctx.respond(embed=embed2, ephemeral=True, delete_after=4) 

def setup(bot):
    bot.add_cog(Moderation(bot))
# This is a cog that adds moderation commands to the bot.

