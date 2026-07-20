import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from scanner import scan

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


def split_message(text: str, max_chars: int = 3500):
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""

    for line in text.splitlines():
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = line

    if current:
        chunks.append(current)

    return chunks


async def send_long_message(update: Update, text: str):
    chunks = split_message(text)
    total = len(chunks)

    for index, chunk in enumerate(chunks, start=1):
        prefix = f"[{index}/{total}] " if total > 1 else ""
        await update.message.reply_text(prefix + chunk)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\nType /scan to scan the market."
    )


async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Scanning market...")

    result = scan()
    await send_long_message(update, result)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan_command))

print("Bot is running...")

app.run_polling()