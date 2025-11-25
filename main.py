import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# --- GENERATOR USERNAME ---
def generate_usernames(word):
    results = set()

    # original
    results.add(word)

    # tambah 1 huruf di setiap posisi
    letters = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(word) + 1):
        for l in letters:
            new = word[:i] + l + word[i:]
            results.add(new)

    # tukar l ↔ i
    swapped = word.replace("l", "i").replace("i", "l")
    results.add(swapped)

    return list(results)


# --- CEK USERNAME ---
def check_username(username):
    url = f"https://t.me/{username}"
    tg_taken = requests.get(url).status_code == 200

    frag = requests.get(f"https://fragment.com/{username}")
    on_fragment = frag.status_code == 200

    if on_fragment:
        return "❓ fragment"
    elif tg_taken:
        return "❌ taken"
    else:
        return "✅ available"


# --- COMMAND: /create ---
async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /create <kata>")
        return

    base = context.args[0]
    usernames = generate_usernames(base)

    formatted = "\n".join([f"@{u}" for u in usernames][:70])

    await update.message.reply_text(
        f"✨ *Generated Usernames for:* `{base}`\n\n{formatted}",
        parse_mode="Markdown"
    )


# --- COMMAND: /check ---
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /check @username1 @username2")
        return

    msg = ""
    for u in context.args:
        username = u.replace("@", "")
        status = check_username(username)
        msg += f"@{username} → {status}\n"

    await update.message.reply_text(msg)


# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif ✓")


# --- RUN BOT ---
def main():
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create", create))
    app.add_handler(CommandHandler("check", check))

    app.run_polling()


if __name__ == "__main__":
    main()
