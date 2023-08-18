import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import json
import platform



class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = commands.when_mentioned_or(PREFIX), intents = discord.Intents().all())
# defining prefix ^    


        self.cogslist = ["cogs.GlobalSlash", "cogs.MainModeration", "cogs.Logger"]
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)
    # load cogs ^

    async def on_ready(self):
        print("")
        print(Fore.WHITE + "----------WELCOME----------")
        print(Fore.WHITE + "It's great to see you again. Sincerely, " + Fore.RED + client.user.name + Fore.WHITE + "!")
        
        print("")
        print(Fore.WHITE + "----------GENERAL----------")         
        prfx = (Back.BLACK + Fore.WHITE + time.strftime("%H:%M:%S CET", time.gmtime()) + Back.RESET + Fore.WHITE + Style.NORMAL)
        print(prfx + " Logged in as " + Fore.RED + client.user.name)
        print(prfx + " Bot ID " + Fore.RED + str(client.user.id))
        print(prfx + " Discord Version " + Fore.RED + discord.__version__)
        print(prfx + " Python Version " + Fore.RED + str(platform.python_version()))

        print("")
        print(Fore.WHITE + "----------INFO----------")        
        synced = await self.tree.sync()
        print(prfx + " Synced " + Fore.RED + str(len(synced)) + " slash commands")
        print(prfx + " Loaded " + Fore.RED + str(len(self.cogslist)) + " cogs")
        
        print("")
        print(Fore.WHITE + "----------STATS----------")
        print(prfx + " Connected to " + Fore.RED + str(len(client.guilds)) + " servers")
        print(prfx + " Latency is " + Fore.RED + str(round(self.latency, 2)) + "s")
        
        await client.change_presence(activity = discord.Activity(name="/help", type=3))
        
        print("")
        print(Fore.WHITE + "Successfully booted up!")
    # print info message to console on boot and set custom activity ^


with open('config.json', 'r') as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]
    PREFIX = data["PREFIX"]
    
client = Client()
# json config data and client defining ^


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found! Try /help")
# command not found error ^


client.run(TOKEN)
# run bot ^