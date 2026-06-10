import os
import asyncio
import discord
from discord.ext import commands

# 1. Define all Gateway Intents necessary for a high-utility bot
intents = discord.Intents.default()
intents.message_content = True  # Required to read text commands
intents.members = True          # Required for moderation & role tracking
intents.guilds = True           # Required for cluster telemetry
intents.invites = True          # Required for invite tracking
intents.presences = True        # Required to track client status structures

# 2. Globally define the bot instance so main() can find it
# Feel free to change the command_prefix to what you prefer (e.g., "!")
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# 3. Retrieve your token from Railway variables safely
TOKEN = os.environ.get("TOKEN")

@bot.event
async def on_ready():
    print(f"🤖 Bot is fully online and unified as: {bot.user.name}")

@bot.event
async def on_message(message):
    # Emergency panic override check
    if getattr(bot, "panic_mode", False) and not await bot.is_owner(message.author):
        return
    await bot.process_commands(message)

# 4. Asynchronous startup wrapper loop
async def main():
    if not TOKEN:
        print("❌ CRITICAL ERROR: 'TOKEN' missing from Railway environment variables.")
        return

    # Automatically sweep directory and load code files
    for filename in os.listdir('./'):
        if filename.endswith('.py') and filename not in ['bot.py', 'checks.py', 'config.py', 'embeds.py']:
            extension_name = filename[:-3]
            try:
                await bot.load_extension(extension_name)
                print(f"✓ Loaded {extension_name}")
            except Exception as e:
                print(f"✗ Failed to load {extension_name}: {e}")

    # Connect to the Discord gateway API structure
    async with bot:
        await bot.start(TOKEN)

# 5. Fire up the application loop execution engine
if __name__ == "__main__":
    asyncio.run(main())
