from openai import OpenAI
from Binance_api import *
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests
from Prompt_template import *
# import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from BTC_weekly import *
from Top_functions import *

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
DEFAULT_MODEL = 'gpt-4-1106-preview'
DEFAULT_VISION_MODEL = 'gpt-4-vision-preview'

# # define GPT function with input prompt and image url
def ask_gpt_vision(messages_list, model=DEFAULT_MODEL):
    response = client.chat.completions.create(
        model=model,
        messages=messages_list,
        max_tokens=3000,
    )
    response_text = response.choices[0].message.content
    return response_text


# # define GPT function with input prompt only
def ask_gpt(prompt, from_id=TG_BOT_OWNER_ID):
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                { 
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            max_tokens=2000,
        )
        return send_msg(response.choices[0].message.content, from_id)
    except: return


def chat_gpt_english(prompt, gpt_model=DEFAULT_MODEL):
    print(f"CALLING: chat_gpt_english() for '{prompt}' ...")
    response = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": ENGLISH_SYSTEM_PROMPT},
            {"role": "user", "content": ENGLISH_USER_PROMPT},
            {"role": "assistant", "content": ENGLISH_ASSISTANT_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content



# Define a function to pull all of the expdenditure records of this year, calculate the total spend of this month and this year
def get_total_spend_of_any_year_any_month(from_id=TG_BOT_OWNER_ID, year=str(datetime.now().year), month=str(datetime.now().month)):
    df = get_all_expenditure_records(from_id)
    # Convert the 'date' column to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert year and month to int
    year = int(year)
    month = int(month)

    # Calculate the total spent of this year (sum the spent of this year)
    total_spend_this_year = df[df['Date'].dt.year == year]['Spent'].sum()

    # Calculate the total spent of this month in this year (sum the spent of this month)
    total_spend_this_month = df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]['Spent'].sum()

    # round the total spend of this year and this month, only show inter.
    total_spend_this_year = format_number(total_spend_this_year)
    total_spend_this_month = format_number(total_spend_this_month)

    # Inform user the total spent of this year and this month
    send_msg(f"Total spent of this year: {total_spend_this_year} usd\nTotal spent of this month: {total_spend_this_month} usd", from_id)

    return total_spend_this_year, total_spend_this_month


# Instert a new row into 'gpt_response' table from input message_id, chat_id, prompt, response
def insert_new_gpt_response_record(from_id, message_id, prompt, response):
    if not message_id or not prompt or not response or not from_id: return

    new_response_dict = {
        'message_id': message_id,
        'from_id': from_id,
        'prompt': prompt,
        'response': response
    }

    df = pd.DataFrame([new_response_dict])
    df.to_sql('gpt_response', engine, if_exists='append', index=False)

    return True


# define a function to read the latest message from 'gpt_response' table
def get_latest_message_from_gpt_response_table():
    query = text("select * from gpt_response where message_id = (select max(message_id) from gpt_response)")
    df = pd.DataFrame(engine.connect().execute(query).fetchall())
    latest_message_dict = df.iloc[-1].to_dict()
    return latest_message_dict


@retry(wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(3))
def run_conversation_with_functions(chat_id=TG_BOT_OWNER_ID, model=DEFAULT_MODEL, image_url=None, prompt = None, message_id=None):

    if not prompt and not image_url: return
    from_id = chat_id

    if image_url: 
        messages_list = [{"role": "system", "content": SYSTEM_PROMPT_WITH_IMAGE_INPUT}]
        prompt = f"{prompt}\nfrom_id: {chat_id}\nimage_url: {image_url}"
        messages_list.append({"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_url}}]})
        send_msg("GPT is reading the image...", chat_id)
        prompt = ask_gpt_vision(messages_list, DEFAULT_VISION_MODEL)

        if "nice picture" in prompt.lower(): return send_msg("Nice picture!", chat_id)

        send_msg(prompt, chat_id)

        prompt = f"{PREFIX_PROMPT_FOR_RECEIPT_PROCESS}\n{prompt}\nimage_url: {image_url}"


    messages_list = [{"role": "system", "content": SYSTEM_PROMPT_TEXT_INPUT}]
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
    if response_message.content: 
        send_msg(response_message.content, chat_id)
        try: insert_new_gpt_response_record(from_id, message_id, prompt, response_message.content)
        except: pass

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
            "get_ignore_list": get_ignore_list,
            "funding_main_transfer_all_usdt": funding_main_transfer_all_usdt,
            "get_btc_data_with_rsi": get_btc_data_with_rsi
        } 

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            need_to_sum = True if function_name == "insert_new_expenditure_record" else need_to_sum

            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            try: function_to_call(**function_args)
            except: pass

            try: insert_new_gpt_response_record(from_id, message_id, prompt, function_name)
            except: pass

        if need_to_sum:
            # Calculate the total spent of this year (sum the spent of this year)
            try: get_total_spend_of_any_year_any_month(from_id=chat_id, year=str(datetime.now().year), month=str(datetime.now().month))
            except: pass


    # Inform user that the function has been called
    # send_msg("ALL DONE!", chat_id)

    return
    

if __name__ == '__main__':
    print("GPT_functions.py is running directly")
    
    # get_total_spend_of_any_year_any_month(from_id=TG_BOT_OWNER_ID, year=str(datetime.now().year), month=str(datetime.now().month))

    try: 
        r = get_latest_message_from_telegram_messages_table()
        print(json.dumps(r, indent=2))
    except: pass

    try:
        r = get_latest_message_from_gpt_response_table()
        print(json.dumps(r, indent=2))
    except: pass