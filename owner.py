import discord
from discord.ext import commands
import checks
from embeds import BotEmbed

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_developer() # ✅ Changed from is_owner to match your checks.py file perfectly
    async def owner_ping(self, ctx):
        """A simple verification command for the main bot owner."""
        await ctx.send(embed=BotEmbed.success("Owner authentication system operational."))

async def setup(bot):
    await bot.add_cog(Owner(bot)) # ✅ Uses correct asynchronous loading format
