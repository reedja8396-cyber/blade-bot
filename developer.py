import discord
from discord.ext import commands
import checks
from embeds import BotEmbed
import psutil
import time

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- LOOKUP & INVESTIGATION TOOLS ---
    @commands.command()
    @checks.is_developer()
    async def lookup(self, ctx, user: discord.User):
        embed = BotEmbed(title=f"🔍 Global Identity Lookup: {user.name}")
        embed.add_field(name="Account Creation", value=discord.utils.format_dt(user.created_at))
        embed.add_field(name="User ID", value=f"`{user.id}`")
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_developer()
    async def addnote(self, ctx, user_id: int, *, note: str):
        if user_id not in self.bot.user_notes:
            self.bot.user_notes[user_id] = []
        self.bot.user_notes[user_id].append(note)
        await ctx.send(embed=BotEmbed.success(f"Added structural note for User ID `{user_id}`."))

    @commands.command()
    @checks.is_developer()
    async def notes(self, ctx, user_id: int):
        notes_list = self.bot.user_notes.get(user_id, [])
        if not notes_list:
            return await ctx.send(embed=BotEmbed.error("No structural data notes found for this user."))
        content = "\n".join([f"- {n}" for n in notes_list])
        await ctx.send(embed=BotEmbed(title=f"📋 Notes Matrix for ID: {user_id}", description=content))

    @commands.command()
    @checks.is_developer()
    async def risk(self, ctx, user_id: int):
        score = self.bot.trust_scores.get(user_id, 50)
        flags = self.bot.user_flags.get(user_id, ["NONE"])
        embed = BotEmbed(title=f"⚠️ Security Risk Profile: {user_id}")
        embed.add_field(name="Trust Rating Matrix", value=f"**{score}/100**")
        embed.add_field(name="Assigned Security Flags", value=", ".join(flags))
        await ctx.send(embed=embed)

    # --- INFRASTRUCTURE & HARDWARE DIAGNOSTICS ---
    @commands.command()
    @checks.is_developer()
    async def bothealth(self, ctx):
        embed = BotEmbed.system("Hardware Engine Health Metrics", "Active platform diagnostics:")
        embed.add_field(name="🧠 Memory Allocation", value=f"`{psutil.virtual_memory().percent}% used`")
        embed.add_field(name="⚙️ CPU Execution Load", value=f"`{psutil.cpu_percent()}% used`")
        embed.add_field(name="🥏 Storage Drive Footprint", value=f"`{psutil.disk_usage('/').percent}% used`")
        embed.add_field(name="📡 API Response Ping", value=f"`{round(self.bot.latency * 1000)}ms`")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_developer()
    async def forcereload(self, ctx):
        await ctx.send("🔄 Force reloading core modules...")
        for ext in ['developer', 'moderation', 'owner', 'logger']:
            await self.bot.reload_extension(ext)
        await ctx.send(embed=BotEmbed.success("All cogs hot-swapped successfully."))

async def setup(bot):
    await bot.add_cog(Developer(bot))
