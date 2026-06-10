import discord
from discord.ext import commands
import checks
from embeds import BotEmbed
import config

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def owneradd(self, ctx, user_id: int):
        config.OWNERS.append(user_id)
        await ctx.send(embed=BotEmbed.success(f"Granted root administrative **Owner** privileges to ID `{user_id}`."))

    @commands.command()
    @checks.is_owner()
    async def panic(self, ctx):
        config.PANIC_MODE = True
        self.bot.panic_mode = True
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="🚨 PANIC MODE LOCKDOWN"))
        await ctx.send(embed=BotEmbed.system("CRITICAL WARNING", "Global bot command processing pathways locked down."))

    @commands.command()
    @checks.is_owner()
    async def panicoff(self, ctx):
        config.PANIC_MODE = False
        self.bot.panic_mode = False
        await self.bot.change_presence(status=discord.Status.online)
        await ctx.send(embed=BotEmbed.success("Panic isolation filter turned off. Resuming normal operations."))

    @commands.command()
    @checks.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("💤 Server connection pipes broken safely. System powering off...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Owner(bot))
