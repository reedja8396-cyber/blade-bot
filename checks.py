import discord
from discord.ext import commands

def is_developer():
    """
    Security check decorator that validates if the command executor 
    matches your exact administrator profile signature.
    """
    async def predicate(ctx):
        # Your exact hardcoded Discord User ID
        AUTHORIZED_DEVELOPER_IDS = [1489289347650949302]
        
        # Check if the user executing the command is in the list
        if ctx.author.id in AUTHORIZED_DEVELOPER_IDS:
            return True
            
        # Log unauthorized attempts to your Railway terminal console
        print(f"🔒 Security Refusal: User {ctx.author} ({ctx.author.id}) attempted administrative commands without clearance.")
        raise commands.CheckFailure("Access Denied: Administrative developer clearance required.")

    return commands.check(predicate)
