# OSINT Domain Checker Telegram Bot
# by SaidSecurity

from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests, time, re
from collections import defaultdict

# User rate limit: {user_id: [count, last_reset_timestamp]}
user_limits = defaultdict(lambda: [0, time.time()])

# SecurityTrails API keys (rotated)
API_KEYS = [
    "YOUR_API_KEY_1",
    "YOUR_API_KEY_2",
    "YOUR_API_KEY_3",
]
current_key_index = 0

# Telegram Bot Token
TG_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

MAX_REQUESTS_PER_DAY = 2
DAY_SECONDS = 86400

# Check if domain format is valid
def is_valid_domain(domain):
    pattern = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None

# Fetch data from SecurityTrails API
def get_data(domain):
    global current_key_index
    while current_key_index < len(API_KEYS):
        try:
            api_key = API_KEYS[current_key_index]
            headers = {"apikey": api_key}
            url = f"https://api.securitytrails.com/v1/domain/{domain}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            elif response.status_code in (429, 403):
                current_key_index += 1
            else:
                return {"error": f"Unexpected error: {response.status_code}"}
        except:
            return {"error": "All API keys exhausted or invalid."}
    return {"error": "All API keys exhausted or invalid."}

async def log_to_admin(application, user_id, username, domain):
    admin_chat_id = 1909135185  # Replace with your admin ID
    text = (
        f"📝 *New Check Request*\n"
        f"• User: `{username}`\n"
        f"• ID: `{user_id}`\n"
        f"• Domain: `{domain}`"
    )
    await application.bot.send_message(chat_id=admin_chat_id, text=text, parse_mode="Markdown")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "> *Welcome to SaidSecurity Domain Checker Bot!*\n\n"
        "> Check DNS, IP, MX, and more details for any domain.\n"
        "> Official contact on LinkedIn:\n    https://www.linkedin.com/in/nursaid-kamilli\n"
        "> Usage:\n"
        "   '/check example.com' to check a domain\n"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_text = (
        "> *Contact me*\n\n"
        "> *@elsenoraccount*\n"
        "> *Website:* saidsecurity.com"
    )
    await update.message.reply_text(contact_text, parse_mode="Markdown")

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()
    count, last_reset = user_limits[user_id]

    if now - last_reset > DAY_SECONDS:
        count = 0
        last_reset = now

    if count >= MAX_REQUESTS_PER_DAY:
        await update.message.reply_text("⚠️ You reached your daily limit of 2 checks.\nPlease try again tomorrow.")
        return

    if not context.args:
        await update.message.reply_text("Please provide a domain. Example:\n/check example.com")
        return

    domain = context.args[0]
    if not is_valid_domain(domain):
        await update.message.reply_text("❌ Invalid domain format.\nPlease provide a correct domain, e.g., example.com")
        return

    user_limits[user_id] = [count + 1, last_reset]

    application = context.application
    username = update.effective_user.username or "NoUsername"
    await log_to_admin(application, user_id, username, domain)

    await update.message.reply_text(f"Checking {domain}...")

    data = get_data(domain)
    if "error" in data:
        await update.message.reply_text(f"Error: {data['error']}")
        return

    text = f"🔎 *Domain Info*\n"
    text += f"Hostname: {data.get('hostname')}\n"
    text += f"Apex domain: {data.get('apex_domain')}\n"

    a_records = data.get("current_dns", {}).get("a", {}).get("values", [])
    if a_records:
        ips = [v['ip'] for v in a_records]
        text += f"• IPv4: `{', '.join(ips)}`\n"

    aaaa_records = data.get("current_dns", {}).get("aaaa", {}).get("values", [])
    if aaaa_records:
        ipsv6 = [v['ipv6'] for v in aaaa_records]
        text += f"IPv6: `{', '.join(ipsv6)}`\n"

    mx_records = data.get("current_dns", {}).get("mx", {}).get("values", [])
    if mx_records:
        mx_hosts = [v['hostname'] for v in mx_records]
        text += f"MX: `{', '.join(mx_hosts)}`\n"

    ns_records = data.get("current_dns", {}).get("ns", {}).get("values", [])
    if ns_records:
        ns = [v['nameserver'] for v in ns_records]
        text += f"NS: `{', '.join(ns)}`\n"

    soa_records = data.get("current_dns", {}).get("soa", {}).get("values", [])
    if soa_records:
        email = soa_records[0].get("email", "N/A")
        text += f"SOA Email: `{email}`\n"

    txt_records = data.get("current_dns", {}).get("txt", {}).get("values", [])
    if txt_records:
        txt_vals = [v['value'] for v in txt_records]
        text += f"TXT: `{', '.join(txt_vals)}`\n"

    sub_count = data.get("subdomain_count", 0)
    text += f"Subdomain count: `{sub_count}`\n"

    await update.message.reply_text(text, parse_mode="Markdown")

async def set_commands(application):
    await application.bot.set_my_commands([
        BotCommand("start", "Welcome and usage info"),
        BotCommand("check", "Check a domain (/check domain.com)"),
        BotCommand("contact", "Contact info"),
    ])

def main():
    app = ApplicationBuilder().token(TG_TOKEN).post_init(set_commands).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(CommandHandler("contact", contact_command))
    print("Bot running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
