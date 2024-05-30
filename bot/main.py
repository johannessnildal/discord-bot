import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
import os
from dotenv import load_dotenv
import glob

load_dotenv()
token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = commands.when_mentioned_or(prefix), intents = discord.Intents.all()) 
# defining prefix ^    

        self.cogslist = []
        for file in glob.glob("cogs/*.py"):
            try:
                ext = file.replace("/", ".").replace("\\", ".")[:-3]
                self.load_extension(ext)
                self.cogslist.append(ext)
            except Exception as e:
                print(f"Failed to load cog {ext}: {e}")
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
                print(prfx + " Loaded " + Fore.BLUE + cog_name)

        print("")
        print(Fore.WHITE + "---------- BOOT ----------")
        print(prfx + Fore.GREEN + " Successfully booted up!" + Style.RESET_ALL)
    # print info message to console on boot and set custom activity ^
    
bot = Client()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="⚠️ Error", 
            description="The command entered does not exist.\nThis message will be deleted shortly.", 
            color=discord.Color.orange(), 
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Try" , value="`/help` to get a list of available commands")
        embed.set_footer(text="Parry | Errors")
        await ctx.send(embed=embed, delete_after=15)
    
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="⛔️ Error", 
            description="You do not have the required permissions to use this command.\nThis message will be deleted shortly.", 
            color=discord.Color.red(), 
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Try" , value="Contact staff or an administrator")
        embed.set_footer(text="Parry | Errors")
        await ctx.send(embed=embed, delete_after=15)
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="⚠️ Error", 
            description="You are missing required arguments.\nThis message will be deleted shortly.", 
            color=discord.Color.orange(), 
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Try" , value="Check the command syntax and try again")
        embed.set_footer(text="Parry | Errors")
        await ctx.send(embed=embed, delete_after=15)
    
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏳ Error", 
            description="This command is on cooldown, please try again later.\nThis message will be deleted shortly.", 
            color=discord.Color.orange(), 
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Try" , value="Wait for the cooldown to expire")
        embed.set_footer(text="Parry | Errors")
        await ctx.send(embed=embed, delete_after=15)
# Error handling ^

bot.run(token)
# run bot ^