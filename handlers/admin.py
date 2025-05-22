from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.date_picker import build_date_picker
from states import DATE_SELECTION, ADMIN_ALTERNATIVE
from services.amadeus import search_flights  # ✅ Import Amadeus flight search

# ✅ Admin review handler
async def handle_admin_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("admin_approve_"):
        _, _, user_id, date = data.split("_")
        user_id = int(user_id)

        # ✅ Notify user
        await context.bot.send_message(chat_id=user_id, text=f"✅ Your flight for {date} has been approved!")

        # ✅ Fetch user route data
        user_data = context.user_data
        origin = user_data.get("origin")
        destination = user_data.get("destination")

        if origin and destination:
            try:
                # ✅ Search for flights using Amadeus
                flights_data = search_flights(origin, destination, date)

                if not flights_data:
                    await context.bot.send_message(chat_id=user_id, text="⚠️ No flights found at this time.")
                else:
                    for offer in flights_data[:3]:  # Show up to 3 offers
                        price = offer["price"]["total"]
                        currency = offer["price"]["currency"]
                        segments = offer["itineraries"][0]["segments"]

                        departure = segments[0]["departure"]
                        arrival = segments[-1]["arrival"]

                        msg = (
                            f"✈️ *Flight Offer*\n"
                            f"From: {departure['iataCode']} at {departure['at']}\n"
                            f"To: {arrival['iataCode']} at {arrival['at']}\n"
                            f"💰 Price: {price} {currency}\n\n"
                            f"Book via airline or contact admin for assistance."
                        )

                        await context.bot.send_message(chat_id=user_id, text=msg, parse_mode='Markdown')
            except Exception as e:
                await context.bot.send_message(chat_id=user_id, text="❌ Failed to fetch flight options.")
                print(f"[ERROR] Amadeus search failed: {e}")
        else:
            await context.bot.send_message(chat_id=user_id, text="⚠️ Missing route info. Please start again.")

        await query.edit_message_text(f"Approved flight for user {user_id} on {date}.")
        return ConversationHandler.END

    elif data.startswith("admin_disapprove_"):
        _, _, user_id = data.split("_")
        await context.bot.send_message(chat_id=int(user_id), text="❌ Your flight booking was disapproved.")
        await context.bot.send_message(
            chat_id=int(user_id),
            text="Please choose a new *departure date*:",
            reply_markup=build_date_picker('departure'),
            parse_mode='Markdown'
        )
        return DATE_SELECTION

    elif data.startswith("admin_suggest_"):
        _, _, user_id = data.split("_")
        context.user_data['alt_suggest_to'] = int(user_id)
        await query.edit_message_text("📅 Select an *alternative date* to suggest:", reply_markup=build_date_picker('alt'))
        return DATE_SELECTION

# ✅ Handle user accepting alternative date
async def handle_alt_acceptance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ Alternative date accepted.")
    return ConversationHandler.END
