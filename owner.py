import psutil 
from discord.ext import commands 
from checks import is_developer 

class Developer(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    @commands.command() 
    @is_developer() 
    async def memory(self, ctx): 
        await ctx.send(f"RAM Usage: {psutil.virtual_memory().percent}%") 

# ◄— Make sure you deleted the extra @commands.command() lines at the bottom!

async def setup(bot):
    await bot.add_cog(Developer(bot))
