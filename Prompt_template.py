from time import strftime, localtime

# Telegram
WELCOME_FROM_TELEGRAM_BOT = "You could ask me anything or send your receipt.\nThis is GPT Assistant developed by \nLEOWANG.net" 

CATEGORIES = ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Rent Mortgage', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Travel', 'Personal Care', 'Home Maintenance', 'Gifts Donations', 'Savings Investments', 'Electronics', 'Kids', 'Pets', 'Fitness', 'Insurance', 'Others']

'''
def get_total_spend_of_any_year_any_month(from_id=os.getenv('TG_BOT_OWNER_ID'), query_year='2023', query_month='12'):
    df = get_all_expenditure_records()
    # Convert the 'date' column to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert query_year and query_month to int
    query_year = int(query_year)
    query_month = int(query_month)

    # Calculate the total spent of this year (sum the spent of this year)
    total_spend_this_year = df[df['Date'].dt.year == query_year]['Spent'].sum()

    # Calculate the total spent of this month in this year (sum the spent of this month)
    total_spend_this_month = df[(df['Date'].dt.year == query_year) & (df['Date'].dt.month == query_month)]['Spent'].sum()

    # round the total spend of this year and this month, only show inter.
    total_spend_this_year = format_number(total_spend_this_year)
    total_spend_this_month = format_number(total_spend_this_month)

    # Inform user the total spent of this year and this month
    send_msg(f"Total spent of this year: {total_spend_this_year} usd\nTotal spent of this month: {total_spend_this_month} usd", from_id)

    return total_spend_this_year, total_spend_this_month
    '''

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
    }, {   
        "type": "function",
        "function": {
            "name": "get_token_price",
            "description": "Get the price of a token from binance API",
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string", "description": "The token symbol in upper case"},
                    "from_id": {"type": "string", "description": "The user's telegram from_id"}
                },
                "required": ["coin", "from_id"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "get_total_spend_of_any_year_any_month",
            "description": "Get the total spend of given year and given month",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_id": {"type": "string", "description": "The user's telegram from_id"},
                    "query_year": {"type": "string", "description": "The year to query, default to current year"},
                    "query_month": {"type": "string", "description": "The month to query, default to current month"},
                },
                "required": ["from_id", "query_year"]
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