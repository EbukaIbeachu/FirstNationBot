from telegram import ReplyKeyboardMarkup

# Centralized IATA airport codes list
IATA_CODES = [
    ["LOS", "ABV", "PHC"],   # Nigeria
    ["ENU", "KAN", "QOW"],
    ["JFK", "LAX", "ORD"],   # USA
    ["ATL", "DFW", "MIA"],
    ["LHR", "LGW", "MAN"],   # UK
    ["CDG", "AMS", "FRA"],   # Europe
    ["DXB", "DOH", "IST"],   # Middle East
    ["PEK", "HND", "SIN"],   # Asia
    ["CPT", "JNB", "NBO"],   # Africa
    ["SYD", "MEL", "AKL"]    # Oceania
]

# Keyboard markup using IATA_CODES
iata_markup = ReplyKeyboardMarkup(
    IATA_CODES,
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder="Choose or type a 3-letter IATA code"
)
