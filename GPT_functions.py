from openai import OpenAI
from Binance_api import *
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests
from Prompt_template import *
import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from BTC_weekly import *

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
DEFAULT_MODEL = 'gpt-4-1106-preview'
DEFAULT_VISION_MODEL = 'gpt-4-vision-preview'

# # define GPT function with input prompt and image url
async def ask_gpt_vision(messages_list, model=DEFAULT_MODEL):
    response = client.chat.completions.create(
        model=model,
        messages=messages_list,
        max_tokens=3000,
    )
    response_text = response.choices[0].message.content
    return response_text


# # define GPT function with input prompt only
async def ask_gpt(prompt, from_id=TG_BOT_OWNER_ID, model=DEFAULT_MODEL):
    response = client.chat.completions.create(
        model=model,
        messages=[
            { 
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
        max_tokens=2000,
    )
    return send_msg(response.choices[0].message.content, from_id)


# Define a function to pull all of the expdenditure records of this year, calculate the total spend of this month and this year
def get_total_spend_of_any_year_any_month(from_id=TG_BOT_OWNER_ID, query_year=str(datetime.now().year), query_month=str(datetime.now().month)):
    df = get_all_expenditure_records(from_id)
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


@retry(wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(3))
async def run_conversation_with_functions(chat_id=TG_BOT_OWNER_ID, model=DEFAULT_MODEL, image_url=None, prompt = None):

    if not prompt and not image_url: return

    if image_url: 
        messages_list = [{"role": "system", "content": SYSTEM_PROMPT_WITH_IMAGE_INPUT}]
        prompt = f"{NO_IMAGE_CAPTION_DEFAULT}\n{prompt}\nfrom_id: {chat_id}\nimage_url: {image_url}"
        messages_list.append({"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_url}}]})
        send_msg("GPT is reading the image...", chat_id)
        prompt = await ask_gpt_vision(messages_list, DEFAULT_VISION_MODEL)

        if "nice picture" in prompt.lower(): return send_msg(prompt, chat_id)

        prompt = f"receipt\n{prompt}\nfrom_id: {chat_id}\nimage_url: {image_url}"
    
    # if not 'receipt' in prompt.lower(): 
    #     await ask_gpt(prompt, chat_id, model)
    #     return 

    messages_list = [{"role": "system", "content": SYSTEM_PROMPT_FOR_PURE_TEXT_INPUT}]
    prompt = f"{prompt}\nfrom_id: {chat_id}\ncurrent_date: {datetime.now().strftime('%Y-%m-%d')}\ncurrent_time: {datetime.now().strftime('%H:%M')}"
    messages_list.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages_list,
        tools=FUNCTIONS_TOOLS,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message

    # If there's content in the response, send it to the user
    if response_message.content: send_msg(response_message.content, chat_id)

    tool_calls = response_message.tool_calls

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        need_to_sum = False
        send_msg('GPT is calling the functions...', chat_id)
        # Step 3: call the function
        available_functions = {
            "insert_new_expenditure_record": insert_new_expenditure_record,
            "get_total_spend_of_any_year_any_month": get_total_spend_of_any_year_any_month,
            "add_coin_to_ignore_list": add_coin_to_ignore_list,
            "get_token_price_from_coinmarketcap_and_send_msg": get_token_price_from_coinmarketcap_and_send_msg,
            "get_ignore_list": get_ignore_list,
            "funding_main_transfer_all_usdt": funding_main_transfer_all_usdt,
            "main_funding_transfer_with_check_and_send": main_funding_transfer_with_check_and_send,
            'get_coin_deposit_address': get_coin_deposit_address,
            "get_btc_data_with_rsi": get_btc_data_with_rsi
        } 
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            need_to_sum = True if function_name == "insert_new_expenditure_record" else need_to_sum

            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            try: function_to_call(**function_args)
            except Exception as e: send_msg(f"Failed from calling '{function_name}()'...\n\n{e}", chat_id)

        if need_to_sum:
            # Calculate the total spent of this year (sum the spent of this year)
            try: get_total_spend_of_any_year_any_month(chat_id, query_year=str(datetime.now().year), query_month=str(datetime.now().month))
            except: pass


    # Inform user that the function has been called
    # send_msg("ALL DONE!", chat_id)

    return
    

if __name__ == '__main__':
    print("GPT_functions.py is running directly")
    
    get_total_spend_of_any_year_any_month(from_id=TG_BOT_OWNER_ID, query_year=str(datetime.now().year), query_month=str(datetime.now().month))