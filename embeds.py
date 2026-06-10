import discord
import datetime

class BotEmbed(discord.Embed):
    def __init__(self, title=None, description=None, color=0x2b2d31, **kwargs):
        super().__init__(title=title, description=description, color=color, **kwargs)
        self.timestamp = datetime.datetime.utcnow()

    @classmethod
    def success(cls, description: str):
        return cls(title="✅ Success", description=description, color=0x2ecc71)

    @classmethod
    def error(cls, description: str):
        return cls(title="❌ Error", description=description, color=0xe74c3c)

    @classmethod
    def system(cls, title: str, description: str):
        return cls(title=f"⚙️ System: {title}", description=description, color=0x34495e)

    @classmethod
    def ai(cls, title: str, description: str):
        return cls(title=f"🤖 AI Analytics: {title}", description=description, color=0x9b59b6)
