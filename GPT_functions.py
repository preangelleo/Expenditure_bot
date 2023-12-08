from openai import OpenAI
from Top_functions import *
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests
from Prompt_template import *

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
DEFAULT_MODEL = 'gpt-4-1106-preview'
DEFAULT_VISION_MODEL = 'gpt-4-vision-preview'

# # define GPT function with input prompt and image url
async def ask_gpt_vision(prompt, image_url, from_id=os.getenv('TG_BOT_OWNER_ID'), model=DEFAULT_MODEL):
    send_msg("GPT is reading the image...", from_id)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=3000,
    )
    response_text = response.choices[0].message.content
    return response_text


# # define GPT function with input prompt only
# def ask_gpt(prompt, from_id=os.getenv('TG_BOT_OWNER_ID'), model=DEFAULT_MODEL):
#     send_telegram_message("GPT is thinking...", from_id)
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             { 
#                 "role": "user",
#                 "content": [{"type": "text", "text": prompt}]
#             }
#         ],
#         max_tokens=2000,
#     )
#     response_text = response.choices[0].message.content
#     return response_text



# @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
# def chat_completion_request(prompt, tools=None, tool_choice=None, model=DEFAULT_MODEL):
#     # print("chat_completion_request() working...")
#     # send_telegram_message("GPT is calling function(s)...", from_id)

#     headers = { "Content-Type": "application/json",  "Authorization": "Bearer " + os.getenv('OPENAI_API_KEY')}
#     json_data = {"model": model, "messages": prompt}
#     if tools is not None: json_data.update({"tools": tools})
#     if tool_choice is not None: json_data.update({"tool_choice": tool_choice})
#     try: return requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
#     except: return 


# def run_gpt_with_function_calls(prompt, from_id=os.getenv('TG_BOT_OWNER_ID')):
#     tools = FUNCTIONS_TOOLS
#     chat_response = chat_completion_request(prompt, tools=tools)
#     assistant_message = chat_response.json()["choices"][0]["message"]
#     '''
#     assistant_message:  {'role': 'assistant', 'content': None, 'tool_calls': [
#         {'id': 'call_6rTbXISyXSLjp8UC0QugIJWZ', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "FLORIDAS NATURAL", "category": "Beverage", "unit_price": 2.5, "units": 2, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, 
#         {'id': 'call_CdSCW8dDlJ3RtgHslWKGvixh', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "LUCERNE WHOLE MILK", "category": "Dairy", "unit_price": 4.99, "units": 1, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, 
#         {'id': 'call_x6Gt63yxtEO4wymAIJSEqAgA', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "BLUEBERRIES ORGNC", "category": "Produce", "unit_price": 8.99, "units": 1, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, 
#         {'id': 'call_ZVF8O00SGFF969u346ufDyXS', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "GALA APPLES LARGE", "category": "Produce", "unit_price": 2.69, "units": 3.96, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, 
#         {'id': 'call_rr0RJIVIHsWAckF8hEO3N2KM', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "GRAPE RD SDLSS ORG", "category": "Produce", "unit_price": 4.99, "units": 2.24, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}
#         ]}'''

#     item_counts = len(assistant_message["tool_calls"])
#     if not item_counts: return

#     i = 0
#     # execut the function calls
#     for tool_call in assistant_message["tool_calls"]:
        
#         if tool_call["type"] == "function":
#             i += 1
#             function_name = tool_call["function"]["name"]
#             send_telegram_message(f"{i}/{item_counts}: Calling '{function_name}()'...", from_id)
#             arguments = tool_call["function"]["arguments"]
#             arguments_dict = json.loads(arguments)

#             if function_name == "insert_expenditure_record":
#                 try: insert_expenditure_record(**arguments_dict)
#                 except Exception as e: send_telegram_message(f"Failed from calling '{function_name}()'...\n\n{e}", from_id)

#     return i


async def run_conversation_with_functions(chat_id=os.getenv('TG_BOT_OWNER_ID'), model=DEFAULT_MODEL, image_url=None, prompt = None):

    if image_url: 
        messages_list = [{"role": "system", "content": SYSTEM_PROMPT_WITH_IMAGE_INPUT}]
        prompt = f"{NO_IMAGE_CAPTION_DEFAULT}\n{prompt}\nfrom_id: {chat_id}\nimage_url: {image_url}"
        messages_list.append({"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_url}}]})
        prompt = await ask_gpt_vision(prompt, image_url, chat_id, DEFAULT_VISION_MODEL)

    messages_list = [{"role": "system", "content": SYSTEM_PROMPT_FOR_PURE_TEXT_INPUT}]
    prompt = f"{prompt}\nfrom_id: {chat_id}"
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
        send_msg('GPT is think how to call the functions...', chat_id)
        # Step 3: call the function
        available_functions = {
            "insert_new_expenditure_record": insert_new_expenditure_record,
        } 
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            try: send_msg(function_to_call(**function_args), chat_id)
            except Exception as e: send_msg(f"Failed from calling '{function_name}()'...\n\n{e}", chat_id)
        
        # Inform user that the function has been called
        send_msg("ALL DONE! Anything else?", chat_id)

    return
    

if __name__ == '__main__':
    print("GPT_functions.py is running directly")