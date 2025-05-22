import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from telegram.error import TelegramError
from config import TELEGRAM_TOKEN
from handlers import start, route, date, admin, callbacks
from states import (
    ROUTE_TYPE, ORIGIN, DESTINATION,
    DATE_SELECTION, RETURN_DATE, ADMIN_REVIEW, ADMIN_ALTERNATIVE
)

# === Logging Configuration ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Create Bot Application ===
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# === Error Handler ===
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error("Exception while handling update:", exc_info=context.error)
    
    if update and hasattr(update, 'message') and update.message:
        try:
            await update.message.reply_text("⚠️ An unexpected error occurred. Please try again later.")
        except Exception as e:
            logging.error(f"Failed to send error message to user: {e}")

# === Conversation Handler ===
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start.start)],
    states={
        ROUTE_TYPE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, start.set_route_type)
        ],
        ORIGIN: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, route.set_origin)
        ],
        DESTINATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, route.set_destination)
        ],
        DATE_SELECTION: [
            # Handles text-based manual input (e.g. "2025-06-01")
            MessageHandler(filters.TEXT & ~filters.COMMAND, date.handle_custom_date),
            # Handles calendar date picker interactions
            CallbackQueryHandler(date.handle_date_callback, pattern=r"^date_"),
        ],
        RETURN_DATE: [
            CallbackQueryHandler(date.handle_date_callback)
        ],
        ADMIN_REVIEW: [
            CallbackQueryHandler(admin.handle_admin_review)
        ],
        ADMIN_ALTERNATIVE: [
            CallbackQueryHandler(admin.handle_alt_acceptance)
        ],
        
    },
    fallbacks=[],
    allow_reentry=True
)

# === Register Handlers ===
app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(callbacks.handle_callbacks))  # Global fallback for extra callback buttons
app.add_error_handler(error_handler)

# === Run Bot ===
if __name__ == "__main__":
    print("🚀 Bot is running...")
    app.run_polling()
