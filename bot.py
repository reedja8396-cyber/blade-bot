import asyncio
import discord
from discord.ext import commands
from config import PREFIX, TOKEN

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

COGS = [
    "utility",
    "moderation",
    "developer",
    "owner"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return await ctx.send("You are not authorized to use this command.")
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("Missing permissions.")
    raise error

async def load():
    for cog in COGS:
        await bot.load_extension(cog)

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())
