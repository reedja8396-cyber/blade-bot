import os
import asyncio
import discord
from discord.ext import commands

# ... (Keep your existing bot = commands.Bot(...) configuration setup up here)

async def main():
    # This automatically loops through your files and loads them as extensions
    for filename in os.listdir('./'):
        if filename.endswith('.py') and filename not in ['bot.py', 'checks.py', 'config.py', 'runtime.txt']:
            extension_name = filename[:-3]
            try:
                await bot.load_extension(extension_name)
                print(f"✓ Loaded {extension_name}")
            except Exception as e:
                print(f"✗ Failed to load {extension_name}: {e}")

    # Start the bot after loading everything
    async with bot:
        await bot.start(TOKEN) # Make sure TOKEN matches your variable name

asyncio.run(main())
