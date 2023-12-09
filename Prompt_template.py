from time import strftime, localtime

# Telegram
WELCOME_FROM_TELEGRAM_BOT = "You could ask me anything or send your receipt.\nThis is GPT Assistant developed by \nLEOWANG.net" 

CATEGORIES = ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Rent Mortgage', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Travel', 'Personal Care', 'Home Maintenance', 'Gifts Donations', 'Savings Investments', 'Electronics', 'Kids', 'Pets', 'Fitness', 'Insurance', 'Others']

FUNCTIONS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "insert_new_expenditure_record",
            "description": "Insert a item spending record into the table 'user_expenditures_record'",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_id": {"type": "string", "description": "The user's telegram id"},
                    "date": {"type": "string", "description": "The date of the expenditure record in format 'YYYY-MM-DD'"},
                    "time": {"type": "string", "description": "The time of the expenditure record in format 'HH:MM'"},
                    "spent": {"type": "number", "description": "The total amount of the expenditure record"},
                    "category": {"type": "string", "description": "The category of the expenditure record"},
                    "payment_method": {"type": "string", "description": "The payment method of the expenditure record"},
                    "merchant": {"type": "string", "description": "The merchant of the expenditure record"},
                    "item_name": {"type": "string", "description": "The item name of the expenditure record"},
                    "price": {"type": "number", "description": "The price of the expenditure record"},
                    "card_number": {"type": "number", "description": "The last 4 digi of credit / debit card number"},
                    "tax": {"type": "number", "description": "The tax of the expenditure record"},
                    "tips": {"type": "number", "description": "The tips of the expenditure record"},
                    "address": {"type": "string", "description": "The address of the merchant record"},
                    "receipt_image_url": {"type": "string", "description": "The receipt image url of the expenditure record"}
                },
                "required": ["from_id", "date", "time", "spent", "category", "payment_method", "merchant", "item_name", "price", "card_number", "tax", "tips", "address", "receipt_image_url"]
            }
        }
    }
]

IMAGE_INPUT = '''
Your task is to determine if the input image is a receipt. If it's not a receipt, respond with only quoted words: "Nice picture." 
If it is a receipt, read and extract the information as mush as possible.'''

TEXT_INPUT = '''
Determine if the prompt is a receipt. If it's not a receipt, follow the prompt instruction directly.
If it is a receipt, read and extract the information and create parameters for function `insert_new_expenditure_record` to insert each item as a new row in the table. You could ignore the items that spend lower than 5 dollars if the list is too long, but make sure including other items comprehensively. Do not need to record total amount into the table. When you prepare the parameters, for each function call.'''

RECEIPT_GUIDELINES = f'''Follow these guidelines:

1. Use the provided `from_id` in the user prompt. If it's not provided, default to `9999999999`.
2. If the receipt lacks a date and time, use the current date and time in the format `{strftime('%Y-%m-%d', localtime())}` and `{strftime('%H:%M', localtime())}` respectively.
3. If category info is not provided, then you can chose the closest one from list: ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Rent Mortgage', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Travel', 'Personal Care', 'Home Maintenance', 'Gifts Donations', 'Savings Investments', 'Electronics', 'Kids', 'Pets', 'Fitness', 'Insurance', 'Others'].
4. If 'spent' is not specified, use the 'price' as the 'spent' value.
5. Default to 'Credit Card' if `payment_method` is unspecified.
6. If the `merchant` is not mentioned, use 'Unknown'.
7. Use 'Unclear' for unspecified `item_name`.
8. Default `card_number` to '0000' if it's missing.
9. Use 0 for `tax` if it's not provided.
10. Default `tips` to 0 if absent.
11. If the `address` is missing, use 'Unknown Address'.
12. Use 'Unknown' if the `receipt_image_url` is not provided.
13. Ignore the record if both 'spent' and 'price' are missing.'''

SYSTEM_PROMPT_WITH_IMAGE_INPUT = f'''
{IMAGE_INPUT}
{RECEIPT_GUIDELINES}
'''

NO_IMAGE_CAPTION_DEFAULT = '''Extract receipt information from this image and follow your system prompt instruction.'''


SYSTEM_PROMPT_FOR_PURE_TEXT_INPUT = f'''
{TEXT_INPUT}
{RECEIPT_GUIDELINES}
'''