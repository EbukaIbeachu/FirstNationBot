from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from states import ORIGIN, DESTINATION, DATE_SELECTION
from utils.iata import iata_markup  # Use centralized keyboard markup


async def set_origin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    origin = update.message.text.strip().upper()

    if len(origin) != 3 or not origin.isalpha():
        await update.message.reply_text("❗ Enter a valid *3-letter IATA code* (e.g. LOS).", parse_mode="Markdown")
        return ORIGIN

    context.user_data["origin"] = origin

    # Use the imported iata_markup directly here for destination selection
    await update.message.reply_text(
        "📍 Enter your *destination city* (3-letter IATA code):",
        reply_markup=iata_markup,
        parse_mode="Markdown"
    )
    return DESTINATION


async def set_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    destination = update.message.text.strip().upper()

    if len(destination) != 3 or not destination.isalpha():
        await update.message.reply_text("❗ Enter a valid *3-letter IATA code* (e.g. ABV).", parse_mode="Markdown")
        return DESTINATION

    context.user_data["destination"] = destination

    await update.message.reply_text(
        "📅 Choose your *departure date* or type a custom one (e.g. 2025-05-30):",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    return DATE_SELECTION
