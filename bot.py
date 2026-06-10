import discord
from discord.ext import commands
import config
import asyncio
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Attach dynamic structures globally
bot.panic_mode = config.PANIC_MODE
bot.watchlist = config.WATCHLIST
bot.trust_scores = config.TRUST_SCORES
bot.user_notes = config.USER_NOTES
bot.user_flags = config.USER_FLAGS

@bot.event
async def on_ready():
    print("=========================================")
    print(f"📡 CLIENT ONLINE: {bot.user.name} ({bot.user.id})")
    print(f"🎚️ DEFAULT PREFIX: '{config.PREFIX}'")
    print("=========================================")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} global Slash commands.")
    except Exception as e:
        print(f"❌ Slash sync failure: {e}")

async def load_extensions():
    # Structural module scripts to load as extensions
    extensions = ['developer', 'moderation', 'owner', 'logger']
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"📦 Module Loaded: {ext}.py")
        except Exception as e:
            print(f"❌ Failed to load {ext}.py: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
