from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from calendar import monthrange


def build_date_picker(prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📅 Today", callback_data=f"{prefix}_day_{datetime.now().strftime('%Y-%m-%d')}"),
            InlineKeyboardButton("📆 Tomorrow", callback_data=f"{prefix}_day_{(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}")
        ],
        [
            InlineKeyboardButton("🗓️ Pick a custom date", callback_data=f"{prefix}_custom")
        ]
    ])


def build_calendar(prefix: str, year: int = None, month: int = None) -> InlineKeyboardMarkup:
    today = datetime.today()
    year = year or today.year
    month = month or today.month

    days_in_month = monthrange(year, month)[1]
    first_weekday = datetime(year, month, 1).weekday()  # Monday = 0

    # Generate calendar grid
    keyboard = []

    # Header with month and year
    keyboard.append([
        InlineKeyboardButton(f"{datetime(year, month, 1).strftime('%B %Y')}", callback_data=f"{prefix}_ignore")
    ])

    # Weekdays header
    keyboard.append([
        InlineKeyboardButton(day, callback_data=f"{prefix}_ignore")
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    ])

    # Days grid
    row = []
    for _ in range(first_weekday):  # fill blank days
        row.append(InlineKeyboardButton(" ", callback_data=f"{prefix}_ignore"))

    for day in range(1, days_in_month + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        row.append(InlineKeyboardButton(str(day), callback_data=f"{prefix}_day_{date_str}"))
        if len(row) == 7:
            keyboard.append(row)
            row = []

    if row:
        while len(row) < 7:
            row.append(InlineKeyboardButton(" ", callback_data=f"{prefix}_ignore"))
        keyboard.append(row)

    # Navigation buttons
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.append([
        InlineKeyboardButton("⬅️", callback_data=f"{prefix}_prev_{prev_year}_{prev_month}"),
        InlineKeyboardButton("❌ Cancel", callback_data=f"{prefix}_cancel"),
        InlineKeyboardButton("➡️", callback_data=f"{prefix}_next_{next_year}_{next_month}")
    ])

    return InlineKeyboardMarkup(keyboard)
