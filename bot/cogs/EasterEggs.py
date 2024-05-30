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
        if message.author.bot:
            return

        if "hello there" in message.content.lower():
            await message.channel.send("General Kenobi!")
        elif "i am your father" in message.content.lower():
            await message.channel.send("Noooooo!")
    # Responds to messages containing some references to Star Wars. ^

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        rude_words = ["stupid", "idiot", "dumb"]
        if any(word in message.content.lower() for word in rude_words):
            insults = [
                "Ye scallywag!",
                "Ye barnacle-covered buffoon!",
                "Ye lily-livered landlubber!",
                "Ye scurvy pirate!",
                "Ye yellow-bellied sea dog!",
                "Ye bilge rat!",
                "Ye hornswaggler!",
                "Ye swindler!",
                "Ye scoundrel!",
                "Ye scallywag!",
                "Ye scurvy dog!"
                "Ye dusty barrel of rum!"
            ]
            await message.channel.send(random.choice(insults))
    # Responds to messages containing rude words with pirate insults ^

def setup(bot):
    bot.add_cog(EasterEggs(bot))
# This is a cog that adds easter eggs to the bot.