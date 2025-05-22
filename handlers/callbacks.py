from telegram import Update
from telegram.ext import ContextTypes

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Generic handler for unexpected callback data
    await query.edit_message_text(f"⚠️ Unrecognized action: `{data}`", parse_mode="Markdown")
