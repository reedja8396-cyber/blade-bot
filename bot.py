import asyncio
import discord
from discord.ext import commands
from config import TOKEN, PREFIX

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

EXTENSIONS = [
    "moderation",
    "developer",
    "owner"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("Bot is online!")

async def load_extensions():
    for extension in EXTENSIONS:
        try:
            await bot.load_extension(extension)
            print(f"✓ Loaded {extension}")
        except Exception as e:
            print(f"✗ Failed to load {extension}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
