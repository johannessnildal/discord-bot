import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
import os
from dotenv import load_dotenv
import glob
import discord
import asyncio

load_dotenv()
token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = commands.when_mentioned_or(prefix), intents = discord.Intents().all()) 
# defining prefix ^    

        self.cogslist = []
        for file in glob.glob("cogs/*.py"):
            cog = file.replace("cogs/", "").replace(".py", "")
            self.cogslist.append(f"cogs.{cog}")

        async def setup_hook(self):
            for ext in self.cogslist:
                await self.load_extension(ext)
        # load cogs dynamically based on files in cogs subfolder ^

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.WHITE + time.strftime("%H:%M:%S CET", time.gmtime()) + Back.RESET + Fore.WHITE + Style.NORMAL)
        print("")
        print(Fore.WHITE + "---------- WELCOME ----------")
        print(Fore.WHITE + "It's great to see you again. Sincerely, " + Fore.RED + bot.user.name + Fore.WHITE + "!")


        print("")
        print(Fore.WHITE + "---------- CONFIG ----------")
        if token is None:
            print(prfx + " API Token was" + Fore.RED + " not" + Fore.WHITE + " loaded. Exiting, try again.")
            exit()
        else:
            print(prfx + " API Token was" + Fore.GREEN + " successfully" + Fore.WHITE + " loaded")
        print (prfx + " Prefix is " + Fore.GREEN + prefix)
        
        print("")
        print(Fore.WHITE + "---------- GENERAL ----------")         
        print(prfx + " Bot ID " + Fore.RED + str(bot.user.id))
        print(prfx + " Discord Version " + Fore.RED + discord.__version__)
        print(prfx + " Python Version " + Fore.RED + str(platform.python_version()))
        print(prfx + " Running on " + Fore.RED + platform.system() + " " + platform.release())
        
        print("")
        print(Fore.WHITE + "---------- STATS ----------")
        print(prfx + " Connected to " + Fore.RED + str(len(bot.guilds)) + " servers")
        print(prfx + " Latency is " + Fore.RED + str(round(self.latency, 2)) + "s")
        
        await bot.change_presence(activity = discord.Activity(name="/help", type=3))
        
        print("")
        if len(self.cogslist) > 0:
            print(Fore.WHITE + "---------- COGS ----------")
            print(prfx + " Loaded " + Fore.RED + str(len(self.cogslist)) + " cog(s)")
            for ext in self.cogslist:
                cog_name = ext.split(".")[-1]
                print(prfx + " Loaded " + Fore.RED + cog_name)
        
        print("")
        print(Fore.WHITE + "---------- COMMANDS ----------")
        print(prfx + " Loaded " + Fore.RED + str(len(bot.commands)) + " command(s)")
        
        print("")
        print(Fore.WHITE + "---------- BOOT ----------")
        print(prfx + Fore.GREEN + " Successfully booted up!" + Style.RESET_ALL)
    # print info message to console on boot and set custom activity ^
    
bot = Client()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="⚠️ Error", description="The bot encountered an error, or the command does not exist", color=discord.Color.orange(), timestamp=ctx.message.created_at)
        embed.add_field(name="Try" , value="`/help` | `/ping`")
        embed.set_footer(text="Parry | Errors")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="⛔️ Error", description="You do not have the required permissions to use this command", color=discord.Color.red(), timestamp=ctx.message.created_at)
        embed.add_field(name="Try" , value="Contacting a server staff or administrator")
        embed.set_footer(text="Parry | Errors")
        await ctx.send(embed=embed)
# Error handling ^

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
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
    embed.add_field(name="" , value="...........................", inline=False)
    embed.add_field(name="" , value="####", inline=False)
    embed.set_footer(text="Parry | Moderation")
    clearmsg = await ctx.send(embed=embed)
    for i in range(20, 0, -1):
        embed.set_field_at(3, name="", value=f"This message will delete itself in {i}s", inline=False)
        await clearmsg.edit(embed=embed)
        await asyncio.sleep(1)
    await clearmsg.delete()
# clear command ^

bot.run(token)
# run bot ^

