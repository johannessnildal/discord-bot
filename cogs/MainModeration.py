from discord.ext import commands

# cog info
# name = "MainModeration"
# main, important moderation commands.


class MainModeration(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        if limit < 1:
            status_msg = await ctx.send("```0 is not a valid number. Please try again.```")
            await status_msg.delete(delay=10)
            return
        else:
            deleted = await ctx.channel.purge(limit=limit)
        if limit < 2:
            status_msg = await ctx.send(f"```Deleted {len(deleted)} message | Requested by {ctx.author.name}```")
        else:
            status_msg = await ctx.send(f"```Deleted {len(deleted)} messages | Requested by {ctx.author.name}```")
        await status_msg.delete(delay=10)
    # purge command - deletes messages (quantity is specified in command seperated by space) from channel ^  

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        overwrite.add_reactions = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"```{channel.name} has been locked.```")
    # lock command - locks channel command was used in ^

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        overwrite.add_reactions = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"```{channel.name} has been unlocked.```")
    # unlock command - unlocks channel command was used in ^


async def setup(client: commands.Bot) -> None:
    await client.add_cog(MainModeration(client))
# setup ^