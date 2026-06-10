import discord
from discord.ext import commands
from embeds import BotEmbed

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- MASSIVE SYSTEM AUDIT TRACKING PIPELINE ---
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        # Look for a specific channel to log mutations
        log_channel = discord.utils.get(message.guild.channels, name="mod-logs")
        if log_channel:
            embed = BotEmbed(title="🗑️ Message Purge Trace", color=0xe74c3c)
            embed.add_field(name="Author Information", value=f"{message.author.mention} ({message.author.id})")
            embed.add_field(name="Deleted Content Block", value=f"```text\n{message.content if message.content else '[No Text Content]'}\n```", inline=False)
            embed.set_footer(text=f"Channel Context: #{message.channel.name}")
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        log_channel = discord.utils.get(before.guild.channels, name="mod-logs")
        if log_channel:
            embed = BotEmbed(title="📝 Message Modification Trace", color=0xf1c40f)
            embed.add_field(name="Author Information", value=f"{before.author.mention} ({before.author.id})")
            embed.add_field(name="Original Content Trace", value=f"```text\n{before.content}\n```", inline=False)
            embed.add_field(name="Updated Content Payload", value=f"```text\n{after.content}\n```", inline=False)
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logger(bot))
