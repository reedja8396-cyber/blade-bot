import discord
from discord.ext import commands
import datetime
import checks
from embeds import BotEmbed

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- SERVER SECURITY UTILITIES ---
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(embed=BotEmbed.success(f"Banned user **{member.name}**."))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason=None):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(embed=BotEmbed.success(f"Unbanned user account profile **{user.name}**."))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(embed=BotEmbed.success(f"Kicked **{member.name}** from workspace server."))

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason=None):
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(embed=BotEmbed.success(f"Timed out user **{member.name}** for {minutes} minutes."))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(embed=BotEmbed.success(f"Purged {len(deleted) - 1} target messages."), delete_after=4)

    # --- ADVANCED STRUCTURAL ROLE CONTROLS ---
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rolehumans(self, ctx, role: discord.Role):
        await ctx.send("⏳ Commencing mass role operations across human index population data...")
        count = 0
        for member in ctx.guild.members:
            if not member.bot and role not in member.roles:
                try:
                    await member.add_roles(role)
                    count += 1
                except: continue
        await ctx.send(embed=BotEmbed.success(f"Successfully embedded role **{role.name}** on {count} humans."))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rolebots(self, ctx, role: discord.Role):
        await ctx.send("⏳ Commencing mass role operations across automated software bots...")
        count = 0
        for member in ctx.guild.members:
            if member.bot and role not in member.roles:
                try:
                    await member.add_roles(role)
                    count += 1
                except: continue
        await ctx.send(embed=BotEmbed.success(f"Successfully embedded role **{role.name}** on {count} bot accounts."))

async def setup(bot):
    await bot.add_cog(Moderation(bot))
