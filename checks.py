from discord.ext import commands
from config import OWNER_IDS, DEVELOPER_IDS

def is_owner():
    async def predicate(ctx):
        if ctx.author.id not in OWNER_IDS:
            raise commands.CheckFailure()
        return True
    return commands.check(predicate)

def is_developer():
    async def predicate(ctx):
        if ctx.author.id not in DEVELOPER_IDS:
            raise commands.CheckFailure()
        return True
    return commands.check(predicate)
