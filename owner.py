import psutil
from discord.ext import commands
from utils.checks import is_developer

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_developer()
    async def memory(self, ctx):
        await ctx.send(f"RAM Usage: {psutil.virtual_memory().percent}%")

    @commands.command()
    @is_developer()
    async def cpu(self, ctx):
        await ctx.send(f"CPU Usage: {psutil.cpu_percent()}%")

async def setup(bot):
    await bot.add_cog(Developer(bot))
