from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from states import ROUTE_TYPE, ORIGIN
from utils.iata import iata_markup  # Use centralized keyboard markup


# Route type prompt
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["One-way", "Return"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome to FirstNation Bot!\n\nPlease choose your *route type*:",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    return ROUTE_TYPE


# After selecting route type
async def set_route_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    route_type = update.message.text.strip().lower()

    if route_type not in ["one-way", "return"]:
        await update.message.reply_text("❗ Please choose *One-way* or *Return*.", parse_mode="Markdown")
        return ROUTE_TYPE

    context.user_data["route_type"] = route_type

    # Use the centralized IATA keyboard markup here
    await update.message.reply_text(
        "🛫 Enter your *departure city* (3-letter IATA code):",
        reply_markup=iata_markup,
        parse_mode="Markdown"
    )
    return ORIGIN
