from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import TelegramError
from datetime import datetime
import logging

from utils.date_picker import build_date_picker, build_calendar
from config import ADMIN_USER_ID
from states import RETURN_DATE, ADMIN_REVIEW, ADMIN_ALTERNATIVE, DATE_SELECTION


# Handles when a user types in a custom date manually
async def handle_custom_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message:
        return

    chat_id = update.message.chat.id
    date_input = update.message.text.strip()

    context.user_data["departure_date"] = date_input

    # Build admin review markup
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"admin_approve_{chat_id}_{date_input}"),
            InlineKeyboardButton("❌ Disapprove", callback_data=f"admin_disapprove_{chat_id}"),
        ],
        [
            InlineKeyboardButton("📅 Suggest Alternative", callback_data=f"admin_suggest_{chat_id}")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    message = (
        f"🛂 *Admin Review*\n\n"
        f"Route: {context.user_data.get('origin')} → {context.user_data.get('destination')}\n"
        f"Date: {date_input}\n"
        f"User ID: {chat_id}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_USER_ID,
            text=message,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    except TelegramError as e:
        logging.error(f"Failed to send message to admin: {e}")

    await update.message.reply_text("🕓 Waiting for admin approval...")
    return ADMIN_REVIEW


# Handles all date picker-related callbacks: today, calendar grid, navigation, etc.
async def handle_date_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    # Launch calendar view
    if data == "date_custom":
        today = datetime.today()
        await query.edit_message_text("📅 Choose a date:")
        await query.edit_message_reply_markup(
            reply_markup=build_calendar(prefix="date", year=today.year, month=today.month)
        )
        return DATE_SELECTION

    # Handle selected date
    elif data.startswith("date_day_"):
        selected_date = data.replace("date_day_", "")
        context.user_data["selected_date"] = selected_date

        await query.edit_message_text(
            f"✅ You selected: {selected_date}\n\n🕓 Waiting for admin approval..."
        )

        chat_id = query.message.chat.id

        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"admin_approve_{chat_id}_{selected_date}"),
                InlineKeyboardButton("❌ Disapprove", callback_data=f"admin_disapprove_{chat_id}"),
            ],
            [
                InlineKeyboardButton("📅 Suggest Alternative", callback_data=f"admin_suggest_{chat_id}")
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=ADMIN_USER_ID,
            text=(
                f"🛂 *Admin Review*\n\n"
                f"Route: {context.user_data.get('origin')} → {context.user_data.get('destination')}\n"
                f"Date: {selected_date}\n"
                f"User ID: {chat_id}"
            ),
            reply_markup=markup,
            parse_mode="Markdown"
        )

        return ADMIN_REVIEW

    # Navigate calendar to previous month
    elif data.startswith("date_prev_"):
        _, _, year, month = data.split("_")
        await query.edit_message_reply_markup(
            reply_markup=build_calendar("date", int(year), int(month))
        )
        return DATE_SELECTION

    # Navigate calendar to next month
    elif data.startswith("date_next_"):
        _, _, year, month = data.split("_")
        await query.edit_message_reply_markup(
            reply_markup=build_calendar("date", int(year), int(month))
        )
        return DATE_SELECTION

    # Cancel calendar interaction
    elif data == "date_cancel":
        await query.edit_message_text("❌ Date selection canceled.")
        return ConversationHandler.END

    return DATE_SELECTION
