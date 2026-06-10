import psutil 
from discord.ext import commands 
from checks import is_developer # ◄— Changed this line

class Developer(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    @commands.command() 
    @is_developer() 
    async def memory(self, ctx): 
        await ctx.send(f"RAM Usage: {psutil.virtual_memory().percent}%") 

    @commands.command() 
    @is_developer()
