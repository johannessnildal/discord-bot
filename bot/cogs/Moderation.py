import discord
from discord.ext import commands
import asyncio
from discord.ui import View
from typing import Union
from datetime import datetime

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

log_channels = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: Union[int, str]):
        
        if amount == "all":
            amount = 400
            await ctx.channel.purge(limit=amount+1)
            embed = discord.Embed(
                title="🗑️ Clear", 
                description="I cleared as many messages as i could boss! I'm tired now...", 
                color=discord.Color.brand_red(), 
                timestamp=ctx.message.created_at
                )
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
                if amount > 400:
                    embed = discord.Embed(
                        title="⚠️ Error", 
                        description="You can't delete more than 400 messages at once!\nThis message will be deleted shortly.", 
                        color=discord.Color.orange(), 
                        timestamp=ctx.message.created_at
                    )
                    embed.set_footer(text="Parry | Errors")
                    await ctx.send(embed=embed, delete_after=15)
                    return
                
                elif amount == 0:
                    embed = discord.Embed(
                        title="⚠️ Error", 
                        description="You have to delete at least one message!\nThis message will be deleted shortly.", 
                        color=discord.Color.orange(), 
                        timestamp=ctx.message.created_at
                    )
                    embed.set_footer(text="Parry | Errors")
                    await ctx.send(embed=embed, delete_after=15)
                    return
                
                elif amount < 0:
                    embed = discord.Embed(
                        title="⚠️ Error", 
                        description="You can't delete a negative amount of messages!\nThis message will be deleted shortly.", 
                        color=discord.Color.orange(), 
                        timestamp=ctx.message.created_at
                    )
                    embed.set_footer(text="Parry | Errors")
                    await ctx.send(embed=embed, delete_after=15)
                    return
                
                await ctx.channel.purge(limit=amount+1)
                embed = discord.Embed(
                    title="🗑️ Clear", 
                    description=f"Deleted **{amount}** message(s)!", 
                    color=discord.Color.brand_red(), 
                    timestamp=ctx.message.created_at
                )
                embed.add_field(name="Moderator", value=ctx.author.mention)
                embed.add_field(name="Channel", value=ctx.channel.mention)
                embed.add_field(name="" , value="####", inline=False)
                embed.set_footer(text=cogname)
                view = DeleteToggleView()
                clearmsg = await ctx.send(embed=embed, view=view)
                for i in range(20, 0, -1):
                    if not view.delete_toggle:
                        # Remove the countdown field
                        embed.remove_field(2)
                        await clearmsg.edit(embed=embed)
                        break
                    embed.set_field_at(2, name="Self-Delete", value=f"This message will delete itself in {i}s", inline=False)
                    await clearmsg.edit(embed=embed)
                    await asyncio.sleep(1)
                
                if view.delete_toggle:
                    await clearmsg.delete()
            except ValueError:
                embed = discord.Embed(
                    title="⚠️ Error", 
                    description="Invalid amount parameter. Please provide a number or 'all'.\nThis message will be deleted shortly.", 
                    color=discord.Color.orange(), 
                    ephemeral=True, 
                    timestamp=ctx.message.created_at
                )
                embed.add_field(name="Examples", value=f"`{ctx.prefix}clear 5`\n`{ctx.prefix}clear all`")
                embed.set_footer("Parry | Errors")
                await ctx.send(embed=embed, delete_after=15)
    # clear command ^

    @commands.slash_command(name="log_channel", description="Set the channel where messages will be logged.")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: discord.TextChannel):
        log_channels[ctx.guild.id] = channel.id
        embed = discord.Embed(
            title="📜 Log Channel", 
            description=f"Log channel set to {channel.mention}.", 
            color=discord.Color.brand_red(), 
        )
        embed.set_footer(text=cogname + " - " + datetime.now().strftime("%d-%m-%y %H:%M"))
        await ctx.respond(embed=embed)

    @set_log_channel.error
    async def set_log_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="⛔️ Error", 
                description="You do not have the required permissions to use this command.\nThis message will be deleted shortly.", 
                color=discord.Color.red(), 
                timestamp=datetime.now()
            )
            embed.add_field(name="Try" , value="Contact staff or an administrator")
            embed.set_footer(text="Parry | Errors")
            await ctx.respond(embed=embed, delete_after=20, ephemeral=True)
    # set_log_channel command ^

    @commands.message_command(name="Log Message")
    @commands.has_permissions(administrator=True)
    async def log_message(self, ctx: commands.Context, message: discord.Message):
        embed = discord.Embed(title="📜 Logged Message", description=message.content, color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
        embed.timestamp = message.created_at
        embed.add_field(name="Message ID", value=message.id)
        embed.add_field(name="Channel", value=message.channel.mention)
        embed.add_field(name="Jump to message", value=f"[Click here]({message.jump_url})", inline=False)
        embed.set_footer(text=f"Logged by {ctx.author.display_name}")

        log_channel_id = log_channels.get(ctx.guild.id)
        if log_channel_id:
            log_channel = ctx.guild.get_channel(log_channel_id)
            
            if log_channel:
                await log_channel.send(embed=embed)  # Send the embed to the log channel
                embed = discord.Embed(
                    title="📜 Message Logged", 
                    description=f"Message by {message.author.mention} has been logged!", 
                    color=discord.Color.brand_red(), 
                )
                embed.add_field(name="Jump to log", value=f"[Click here]({log_channel.jump_url})", inline=False)
                embed.set_footer(text=cogname + " - " + datetime.now().strftime("%d-%m-%y %H:%M"))
                await ctx.respond(embed=embed)
            
            else:
                embed = discord.Embed(
                    title="⚠️ Error", 
                    description="Log channel not found. Please set a log channel using `/log_channel`.\nThis message will be deleted shortly.", 
                    color=discord.Color.orange(), 
                )
                embed.set_footer(text="Parry | Errors")
                await ctx.respond(embed=embed, ephemeral=True, delete_after=15)
        
        else:
            embed = discord.Embed(
                title="⚠️ Error", 
                description="Log channel not set. Please set a log channel using `/log_channel`.\nThis message will be deleted shortly.", 
                color=discord.Color.orange(), 
            )
            embed.set_footer(text="Parry | Errors")
            await ctx.respond(embed=embed, ephemeral=True, delete_after=15)
    
    @log_message.error
    async def log_message_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="⛔️ Error", 
                description="You do not have the required permissions to use this command.\nThis message will be deleted shortly.", 
                color=discord.Color.red(), 
                timestamp=datetime.now()
            )
            embed.add_field(name="Try" , value="Contact staff or an administrator")
            embed.set_footer(text="Parry | Errors")
            await ctx.respond(embed=embed, delete_after=20, ephemeral=True)
    # log_message command ^

def setup(bot):
    bot.add_cog(Moderation(bot))
# This is a cog that adds moderation commands to the bot.