import os

# Base Token and Credentials
TOKEN = "YOUR_BOT_TOKEN_HERE"
PREFIX = ","

# Global Permissions Hierarchy
OWNERS = [1489289347650949302]        # Add Discord User IDs for Bot Owners
DEVELOPERS = [1489289347650949302]    # Add Discord User IDs for Developers
PREMIUM_GUILDS = []                  # Add Server IDs with Premium Perks Enabled
PREMIUM_USERS = []                   # Add User IDs with Premium Perks Enabled

# Global Security Settings
PANIC_MODE = False
ANTI_INVITE = True
ANTI_LINK = True
ANTI_SPAM_LIMIT = 5                  # Messages allowed per 5 seconds

# Storage / Diagnostics Framework
WATCHLIST = []                       # List of User IDs under surveillance
TRUST_SCORES = {}                    # Format: {user_id: score_int}
USER_NOTES = {}                      # Format: {user_id: ["note1", "note2"]}
USER_FLAGS = {}                      # Format: {user_id: ["FLAG_NAME"]}

# API Credentials (If using AI Features)
OPENAI_API_KEY = "sk-..."
