import os

# --- RAILWAY ENVIRONMENT VARIABLES ---
# os.getenv pulls the value directly from your Railway Variables tab
TOKEN = os.getenv("TOKEN") 
PREFIX = ","

# --- GLOBAL PERMISSIONS HIERARCHY ---
# Note: Put your Discord User ID integers inside these brackets
OWNERS = []         # Add Discord User IDs for Bot Owners (e.g., [123456789])
DEVELOPERS = []     # Add Discord User IDs for Developers

# --- PREMIUM SYSTEM ENTRIES ---
PREMIUM_GUILDS = [] # Add Server IDs with Premium Perks Enabled
PREMIUM_USERS = []  # Add User IDs with Premium Perks Enabled

# --- GLOBAL SECURITY SETTINGS ---
PANIC_MODE = False
ANTI_INVITE = True
ANTI_LINK = True
ANTI_SPAM_LIMIT = 5 # Messages allowed per 5 seconds

# --- STORAGE / DIAGNOSTICS FRAMEWORK ---
WATCHLIST = []      # List of User IDs under surveillance
TRUST_SCORES = {}   # Format: {user_id: score_int}
USER_NOTES = {}     # Format: {user_id: ["note1", "note2"]}
USER_FLAGS = {}     # Format: {user_id: ["FLAG_NAME"]}

# --- OPTIONAL AI CREDENTIALS ---
# If you add an OpenAI key in Railway variables, it will automatically connect here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...")
