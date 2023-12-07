from time import strftime, localtime

# Telegram
WELCOME_FROM_TELEGRAM_BOT = "You could ask me anything:-) \nThis is GPT Assistant developed by \nLEOWANG.net" 

# GPT Prompt Template
RECEIPT_EXTRACTOR_PROMPT = f"You will extract the purchase information from the user prompt and call the insert_expenditure_record function to insert record into the expenditure_table one by one. You will do this job in just one prompt, so don't ask user for any clarification. Default currency is USD. Put 0 or None for the fields that are not available. If you find no date and time infor, then date is {strftime('%Y-%m-%d', localtime())} and time is {strftime('%H:%M', localtime())}."

READ_RECEIPT = "Read the image and try to find out the detailed information of: item, category, unit_price, units, date, time, currency, tax, tips. The tell me the purchased information in a list."