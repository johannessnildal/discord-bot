import discord
from discord.ext import commands
import discord
from discord.ext import commands
import random

bot = discord.Bot()

cogname = "Parry | Easter Eggs"

class EasterEggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        rude_words = ["stupid", "idiot", "dumb", "ugly", "loser"]
        if any(word in message.content.lower() for word in rude_words):
            if "parry" in message.content.lower():
                insults = [
                    "scallywag!",
                    "barnacle-covered buffoon!",
                    "lily-livered landlubber!",
                    "scurvy pirate!",
                    "yellow-bellied sea dog!",
                    "bilge rat!",
                    "hornswaggler!",
                    "swindler!",
                    "scoundrel!",
                    "scallywag!",
                    "scurvy dog!",
                    "dusty barrel of rum!"
                ]
                await message.channel.send("Shut up ya " + random.choice(insults))
    # Responds to messages containing rude words with responses as pirate insults ^

        if "hello there" in message.content.lower():
            await message.channel.send("General Kenobi!")
        
        elif "i am your father" in message.content.lower():
            await message.channel.send("Noooooo!")
    # Responds to messages containing some references to Star Wars. ^

def setup(bot):
    bot.add_cog(EasterEggs(bot))
# This is a cog that adds easter eggs to the bot.