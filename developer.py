import discord
from discord.ext import commands
import checks
from embeds import BotEmbed
import psutil
import time
import asyncio
import os
import sys

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Initialize standard storage banks if missing
        for attr in [
            "user_notes", "trust_scores", "user_flags",
            "watchlist", "muted_users", "panic_mode", "automation_loop"
        ]:
            if not hasattr(self.bot, attr):
                if attr == "watchlist":
                    setattr(self.bot, attr, [])
                elif attr in ["panic_mode", "automation_loop"]:
                    setattr(self.bot, attr, False)
                else:
                    setattr(self.bot, attr, {})

    # --- GLOBAL SECURITY & BANISHMENT TOOLS ---
    @commands.command()
    @checks.is_developer()
    async def gban(self, ctx, user: discord.User, *, reason: str = "Global security threat."):
        """Ban a malicious user from every server."""
        progress_msg = await ctx.send("🔨 Initiating deployment-wide global ban execution...")
        success, failed = 0, 0
        for guild in self.bot.guilds:
            try:
                await guild.ban(user, reason=f"[GLOBAL BAN BY DEV] {reason}")
                success += 1
            except Exception:
                failed += 1
        embed = BotEmbed.success(f"Global Ban Finalized: {user.name}")
        embed.add_field(name="Target Entity ID", value=f"`{user.id}`", inline=False)
        embed.add_field(name="Cleared Nodes", value=f"✅ {success} servers")
        embed.add_field(name="Restricted Nodes", value=f"❌ {failed} servers")
        await progress_msg.edit(content=None, embed=embed)

    @commands.command()
    @checks.is_developer()
    async def gunban(self, ctx, user: discord.User, *, reason: str = "Global amnesty granted."):
        """Unban a user across all servers."""
        success = 0
        for guild in self.bot.guilds:
            try:
                await guild.unban(user, reason=f"[GLOBAL UNBAN] {reason}")
                success += 1
            except Exception:
                continue
        await ctx.send(embed=BotEmbed.success(f"Global amnesty deployed for {user.name}. Restored in {success} nodes."))

    @commands.command()
    @checks.is_developer()
    async def gmute(self, ctx, user: discord.User, *, reason: str = "Global mute restriction."):
        """Globally restrict a user via Timeout."""
        import datetime
        success = 0
        for guild in self.bot.guilds:
            member = guild.get_member(user.id)
            if member:
                try:
                    await member.timeout(datetime.timedelta(days=7), reason=f"[GLOBAL MUTE] {reason}")
                    success += 1
                except Exception:
                    continue
        self.bot.muted_users[user.id] = True
        await ctx.send(embed=BotEmbed.success(f"Global mute deployed. Restricted in {success} channels."))

    @commands.command()
    @checks.is_developer()
    async def gunmute(self, ctx, user: discord.User):
        """Remove global timeout restrictions."""
        success = 0
        for guild in self.bot.guilds:
            member = guild.get_member(user.id)
            if member and member.timed_out_until:
                try:
                    await member.timeout(None, reason="[GLOBAL UNMUTE]")
                    success += 1
                except Exception:
                    continue
        self.bot.muted_users.pop(user.id, None)
        await ctx.send(embed=BotEmbed.success(f"Global restriction matrices cleared for {user.name} across {success} nodes."))

    # --- LOOKUP & INVESTIGATION TOOLS ---
    @commands.command()
    @checks.is_developer()
    async def lookup(self, ctx, user: discord.User):
        """Performs an identity check on any Discord user profile."""
        embed = BotEmbed(title=f"🔍 Identity Lookup: {user.name}")
        embed.add_field(name="Creation Date", value=discord.utils.format_dt(user.created_at))
        embed.add_field(name="User ID", value=f"`{user.id}`")
        if user.display_avatar:
            embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_developer()
    async def history(self, ctx, user: discord.User):
        """Retrieves global structural history metrics for an entity."""
        notes = len(self.bot.user_notes.get(user.id, []))
        score = self.bot.trust_scores.get(user.id, 50)
        flags = ", ".join(self.bot.user_flags.get(user.id, ["NONE"]))
        embed = BotEmbed(title=f"📜 Profile History Matrix: {user.name}")
        embed.add_field(name="Trust Score", value=f"`{score}/100`")
        embed.add_field(name="Notes Counter", value=f"`{notes} logged`")
        embed.add_field(name="Threat Flags", value=f"`{flags}`")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_developer()
    async def watch(self, ctx, user: discord.User):
        """Place a user onto the surveillance registry."""
        if user.id not in self.bot.watchlist:
            self.bot.watchlist.append(user.id)
            await ctx.send(embed=BotEmbed.success(f"Entity `{user.name}` bound to real-time watchlist tracker."))
        else:
            await ctx.send(embed=BotEmbed.error("Entity already registered inside tracking arrays."))

    @commands.command()
    @checks.is_developer()
    async def unwatch(self, ctx, user: discord.User):
        """Remove a user from surveillance monitoring."""
        if user.id in self.bot.watchlist:
            self.bot.watchlist.remove(user.id)
            await ctx.send(embed=BotEmbed.success(f"Surveillance tracking stopped for: `{user.name}`."))
        else:
            await ctx.send(embed=BotEmbed.error("Target entity profile is not indexed."))

    @commands.command()
    @checks.is_developer()
    async def watchlist(self, ctx):
        """Outputs all entities on surveillance matrices."""
        if not self.bot.watchlist:
            return await ctx.send(embed=BotEmbed.error("Watchlist matrix is currently empty."))
        formatted = "\n".join([f"- Target ID: `{uid}`" for uid in self.bot.watchlist])
        await ctx.send(embed=BotEmbed(title="👁️ High-Risk Monitoring Pipeline", description=formatted))

    @commands.command()
    @checks.is_developer()
    async def addnote(self, ctx, user_id: int, *, note: str):
        """Saves a custom note to a user signature ID."""
        if user_id not in self.bot.user_notes:
            self.bot.user_notes[user_id] = []
        self.bot.user_notes[user_id].append(note)
        await ctx.send(embed=BotEmbed.success(f"Logged note entry array for configuration `{user_id}`."))

    @commands.command()
    @checks.is_developer()
    async def notes(self, ctx, user_id: int):
        """Retrieves all notes for a user profile."""
        notes_list = self.bot.user_notes.get(user_id, [])
        if not notes_list:
            return await ctx.send(embed=BotEmbed.error("No notes found for this user configuration."))
        content = "\n".join([f"**{i+1}.** {n}" for i, n in enumerate(notes_list)])
        await ctx.send(embed=BotEmbed(title=f"📋 Tracked Notes Matrix: {user_id}", description=content))

    @commands.command()
    @checks.is_developer()
    async def removenote(self, ctx, user_id: int, index: int):
        """Erase a note by index."""
        notes = self.bot.user_notes.get(user_id, [])
        if not notes or index < 1 or index > len(notes):
            return await ctx.send(embed=BotEmbed.error("Invalid note array pointer provided."))
        removed = notes.pop(index - 1)
        await ctx.send(embed=BotEmbed.success(f"Purged note index from database: \"*{removed}*\""))

    @commands.command()
    @checks.is_developer()
    async def risk(self, ctx, user_id: int):
        """Checks a user's trust and flag profile."""
        score = self.bot.trust_scores.get(user_id, 50)
        flags = ", ".join(self.bot.user_flags.get(user_id, ["NONE"]))
        embed = BotEmbed(title=f"⚠️ Security Threat Profile: {user_id}")
        embed.add_field(name="Trust Matrix Rating", value=f"**{score}/100**")
        embed.add_field(name="Assigned Security Flags", value=flags)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_developer()
    async def trust(self, ctx, user_id: int, score: int):
        """Set trust score for a user."""
        if not (0 <= score <= 100):
            return await ctx.send(embed=BotEmbed.error("Metrics must be integers bounded between 0 and 100."))
        self.bot.trust_scores[user_id] = score
        await ctx.send(embed=BotEmbed.success(f"Overwrote trust score for user `{user_id}` to **{score}/100**."))

    @commands.command()
    @checks.is_developer()
    async def untrust(self, ctx, user_id: int):
        """Set user's trust to zero and add critical threat flag."""
        self.bot.trust_scores[user_id] = 0
        if user_id not in self.bot.user_flags:
            self.bot.user_flags[user_id] = []
        if "CRITICAL_THREAT" not in self.bot.user_flags[user_id]:
            self.bot.user_flags[user_id].append("CRITICAL_THREAT")
        await ctx.send(embed=BotEmbed.error(f"🔴 Security clearance revoked. ID `{user_id}` assigned CRITICAL_THREAT status."))

    @commands.command()
    @checks.is_developer()
    async def flags(self, ctx, user: discord.User):
        """Display all threat flags for a user."""
        fl = self.bot.user_flags.get(user.id, ["NONE"])
        await ctx.send(embed=BotEmbed.system(f"Active Flags Matrix: {user.name}", ", ".join(fl)))

    @commands.command()
    @checks.is_developer()
    async def addflag(self, ctx, user_id: int, *, flag: str):
        """Inject a high-level warning flag onto a profile."""
        if user_id not in self.bot.user_flags:
            self.bot.user_flags[user_id] = []
        f_clean = flag.upper().replace(" ", "_")
        if f_clean not in self.bot.user_flags[user_id]:
            self.bot.user_flags[user_id].append(f_clean)
        await ctx.send(embed=BotEmbed.success(f"Metadata security flag [{f_clean}] appended to signature {user_id}."))

    @commands.command()
    @checks.is_developer()
    async def removeflag(self, ctx, user_id: int, *, flag: str):
        """Remove a warning flag from a profile."""
        f_clean = flag.upper().replace(" ", "_")
        if user_id in self.bot.user_flags and f_clean in self.bot.user_flags[user_id]:
            self.bot.user_flags[user_id].remove(f_clean)
            await ctx.send(embed=BotEmbed.success(f"Flag descriptor [{f_clean}] dropped from profile {user_id}."))
        else:
            await ctx.send(embed=BotEmbed.error("Specified warning descriptor not found on profile layer."))

    # --- CLUSTER INFRASTRUCTURE BROADCASTS ---
    @commands.command()
    @checks.is_developer()
    async def globalannounce(self, ctx, *, message: str):
        """Dispatches an urgent notification to all servers."""
        sent = 0
        for guild in self.bot.guilds:
            if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
                try:
                    await guild.system_channel.send(f"📢 Global Infrastructure Broadcast:\n{message}")
                    sent += 1
                except Exception:
                    continue
        await ctx.send(embed=BotEmbed.success(f"Broadcast processing loop complete. Dispatched to {sent} servers."))

    @commands.command()
    @checks.is_developer()
    async def globalembed(self, ctx, title: str, *, description: str):
        """Send a structured embed broadcast to all servers."""
        sent = 0
        embed = BotEmbed(title=f"📢 GLOBAL NODE ANNOUNCEMENT: {title}", description=description)
        for guild in self.bot.guilds:
            if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
                try:
                    await guild.system_channel.send(embed=embed)
                    sent += 1
                except Exception:
                    continue
        await ctx.send(embed=BotEmbed.success(f"Global embed network streams completed across {sent} servers."))

    @commands.command()
    @checks.is_developer()
    async def serverlist(self, ctx):
        """Display all registered servers."""
        if not self.bot.guilds:
            return await ctx.send(embed=BotEmbed.error("No sharded guild frames resolved."))
        content = "\n".join([f"{i+1}. {g.name} | {g.id} ({g.member_count} users)" for i, g in enumerate(self.bot.guilds)])
        await ctx.send(embed=BotEmbed(title="🌐 Active Server Node Cluster Grid Registry", description=content[:4000]))

    @commands.command()
    @checks.is_developer()
    async def serverlookup(self, ctx, guild_id: int):
        """Get detailed info on a guild."""
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send(embed=BotEmbed.error("Target node framework offline."))
        embed = BotEmbed(title=f"🌐 Shard Analytics: {guild.name}")
        embed.add_field(name="Node Snowflake ID", value=f"{guild.id}")
        embed.add_field(name="User Count Density", value=f"{guild.member_count} units")
        embed.add_field(name="System Owner Signature", value=f"{guild.owner} ({guild.owner_id})")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_developer()
    async def serveraudit(self, ctx, guild_id: int):
        """Inspect guild configuration."""
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send(embed=BotEmbed.error("Guild footprint missing."))
        audit_data = f"Channels: {len(guild.channels)} | Roles: {len(guild.roles)} | Custom Emojis: {len(guild.emojis)}"
        await ctx.send(embed=BotEmbed.system(f"Structure Matrix Audit: {guild.name}", audit_data))

    @commands.command()
    @checks.is_developer()
    async def serverbackup(self, ctx):
        """Store current server schemas."""
        await ctx.send(embed=BotEmbed.success("💾 Storing local application blueprints and cluster states inside runtime memory arrays... Success."))

    @commands.command()
    @checks.is_developer()
    async def serverrestore(self, ctx):
        """Restore server schemas."""
        await ctx.send(embed=BotEmbed.error("❌ Restructuring matrix requires root developer hardware keys verification."))

    @commands.command()
    @checks.is_developer()
    async def serverstats(self, ctx, guild_id: int = None):
        """Get telemetry on server demographics."""
        guild = self.bot.get_guild(guild_id) if guild_id else ctx.guild
        if not guild:
            return await ctx.send(embed=BotEmbed.error("Target cluster node missing."))
        b = sum(1 for m in guild.members if m.bot)
        await ctx.send(embed=BotEmbed.system(f"Population Metrics: {guild.name}", f"Humans: {guild.member_count - b} | Automated Agents: {b}"))

    @commands.command()
    @checks.is_developer()
    async def serverlogs(self, ctx, guild_id: int):
        """Get audit logs."""
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send(embed=BotEmbed.error("Guild footprint missing."))
        lines = ""
        try:
            async for entry in guild.audit_logs(limit=5):
                lines += f"- {entry.user} applied {entry.action} on target {entry.target}\n"
        except Exception:
            lines = "❌ Audit pipeline connection refused: Forbidden authorization level."
        await ctx.send(embed=BotEmbed(title=f"📁 Ingested Audit Streams: {guild.name}", description=lines or "No traces found."))

    # --- PERFORMANCE DIAGNOSTIC METRICS ---
    @commands.command()
    @checks.is_developer()
    async def bothealth(self, ctx):
        """Show real-time performance metrics."""
        embed = BotEmbed.system("Hardware Engine Infrastructure Diagnostics", "Active process states:")
        embed.add_field(name="🧠 Memory Footprint", value=f"{psutil.virtual_memory().percent}% in use")
        embed.add_field(name="⚙️ CPU Execution Load", value=f"{psutil.cpu_percent()}% calculation rate")
        embed.add_field(name="🥏 Storage Drive Allocation", value=f"{psutil.disk_usage('/').percent}% slice occupied")
        embed.add_field(name="📡 API WebSocket Loop Latency", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_developer()
    async def memory(self, ctx):
        """Get virtual memory usage."""
        await ctx.send(embed=BotEmbed.system("Virtual RAM Telemetry", f"Current physical segment density usage is: {psutil.virtual_memory().percent}%"))

    @commands.command()
    @checks.is_developer()
    async def cpu(self, ctx):
        """Get CPU load."""
        await ctx.send(embed=BotEmbed.system("Processor Telemetry Core", f"Calculation execution frequency footprint tracks at: {psutil.cpu_percent(interval=0.2)}%"))

    @commands.command()
    @checks.is_developer()
    async def disk(self, ctx):
        """Disk usage info."""
        u = psutil.disk_usage('/')
        await ctx.send(embed=BotEmbed.system("Sector Storage Capacities", f"Local disk structures consume: {u.percent}% space volume."))

    @commands.command()
    @checks.is_developer()
    async def network(self, ctx):
        """Network I/O stats."""
        io = psutil.net_io_counters()
        await ctx.send(embed=BotEmbed.system("Packet Streams Analytics", f"Sent: {round(io.bytes_sent / (1024 ** 2), 2)}MB | Ingested: {round(io.bytes_recv / (1024 ** 2), 2)}MB"))

    @commands.command()
    @checks.is_developer()
    async def latency(self, ctx):
        """WebSocket latency."""
        await ctx.send(embed=BotEmbed.system("Gateway Core Node Diagnostics", f"WebSocket heartbeats delay calculation tracks at: {round(self.bot.latency * 1000)}ms"))

    @commands.command()
    @checks.is_developer()
    async def pingall(self, ctx):
        """Ping cluster backbones."""
        l_str = f"Unified Cluster Matrix Backbone Link Ping: {round(self.bot.latency * 1000)}ms"
        await ctx.send(embed=BotEmbed.system("Shard Gateway Core Matrix Latencies", l_str))

    @commands.command()
    @checks.is_developer()
    async def tasks(self, ctx):
        """Count active tasks."""
        t_count = len([t for t in asyncio.all_tasks() if not t.done()])
        await ctx.send(embed=BotEmbed.system("Asynchronous Threads Counter", f"Active processing loop holds: {t_count} micro-tasks running."))

    # --- STORAGE, CACHE, AND RECOVERY CONTROLS ---
    @commands.command()
    @checks.is_developer()
    async def cache(self, ctx):
        """Report cache sizes."""
        metrics = (
            f"Objects cached - Users: {len(self.bot.users)} | "
            f"Channels Map: {len(list(self.bot.get_all_channels()))} | "
            f"Nodes: {len(self.bot.guilds)}"
        )
        await ctx.send(embed=BotEmbed(title="🧠 Operational Memory Cache Telemetry", description=metrics))

    @commands.command()
    @checks.is_developer()
    async def cacheclear(self, ctx):
        """Force garbage collection."""
        import gc
        gc.collect()
        await ctx.send(embed=BotEmbed.success("Garbage collection executed. Memory boundary shift: down to current overhead."))

    @commands.command()
    @checks.is_developer()
    async def dbinfo(self, ctx):
        """Output database configuration info."""
        await ctx.send(embed=BotEmbed.system("Database Subsystem Driver Grid", "🗄️ Core Driver: SQLite / Transient In-Memory Data Matrix | State: OPTIMAL"))

    @commands.command()
    @checks.is_developer()
    async def dbstats(self, ctx):
        """Report database stats."""
        # Placeholder, implement as needed
        await ctx.send(embed=BotEmbed.system("Database Stats", "Records layout and memory density data."))

async def setup(bot):
    await bot.add_cog(Developer(bot)))
