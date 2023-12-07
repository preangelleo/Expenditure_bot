from openai import OpenAI
from Database_api import *
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests

load_dotenv()

client = OpenAI(
  api_key=os.getenv('OPENAI_API_KEY'),
)

# define GPT function with input prompt and image url
def ask_gpt_vision(prompt, image_url):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
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

# define GPT function with input prompt only
def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ],
            }
        ],
        max_tokens=3000,
    )
    response_text = response.choices[0].message.content
    return response_text

# response_text = ask_gpt("How are you doing today?")
# print(response_text)

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model='gpt-4-1106-preview', from_id=os.getenv('TG_BOT_OWNER_ID')):
    # print("chat_completion_request() working...")
    send_telegram_message("GPT is calling function(s)...", from_id)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv('OPENAI_API_KEY'),
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        # print("Unable to generate ChatCompletion response")
        # print(f"Exception: {e}")
        send_telegram_message(f"GPT calling functions(s) failed...\n\n{e}", from_id)

        return e


def run_gpt_with_function_calls(messages, from_id=os.getenv('TG_BOT_OWNER_ID')):
    tools = [
        {"type": "function",
          "function": {
              "name": "insert_expenditure_record",
              "description": "Insert a record into the expenditure_table",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "item": {"type": "string", "description": "The item name"},
                      "category": {"type": "string", "description": "The category of the item"},
                      "unit_price": {"type": "number", "description": "The unit price of the item"},
                      "units": {"type": "number", "description": "The units of the item"},
                      "date": {"type": "string", "description": "The date of the item"},
                      "time": {"type": "string", "description": "The time of the item"},
                      "currency": {"type": "string", "description": "The currency of the item"},
                      "tax": {"type": "number", "description": "The tax of the item"},
                      "tips": {"type": "number", "description": "The tips of the item"}
                  },
                  "required": ["item", "category", "unit_price", "units", "date", "time", "currency", "tax", "tips"]
              }
          }
        }
      ]
    chat_response = chat_completion_request(messages, tools=tools)
    assistant_message = chat_response.json()["choices"][0]["message"]
    # print('assistant_message: ', assistant_message)
    '''
    assistant_message:  {'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'call_6rTbXISyXSLjp8UC0QugIJWZ', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "FLORIDAS NATURAL", "category": "Beverage", "unit_price": 2.5, "units": 2, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, {'id': 'call_CdSCW8dDlJ3RtgHslWKGvixh', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "LUCERNE WHOLE MILK", "category": "Dairy", "unit_price": 4.99, "units": 1, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, {'id': 'call_x6Gt63yxtEO4wymAIJSEqAgA', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "BLUEBERRIES ORGNC", "category": "Produce", "unit_price": 8.99, "units": 1, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, {'id': 'call_ZVF8O00SGFF969u346ufDyXS', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "GALA APPLES LARGE", "category": "Produce", "unit_price": 2.69, "units": 3.96, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}, {'id': 'call_rr0RJIVIHsWAckF8hEO3N2KM', 'type': 'function', 'function': {'name': 'insert_expenditure_record', 'arguments': '{"item": "GRAPE RD SDLSS ORG", "category": "Produce", "unit_price": 4.99, "units": 2.24, "date": "Unknown", "time": "Unknown", "currency": "Unknown", "tax": 0.0, "tips": 0.0}'}}]}'''

    ittem_counts = 0
    # execut the function calls
    for tool_call in assistant_message["tool_calls"]:
        send_telegram_message(f"Inserting new items to expenditure table...", from_id)
        ittem_counts = len(assistant_message["tool_calls"])
        if tool_call["type"] == "function":
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]
            arguments_dict = json.loads(arguments)
            if function_name == "insert_expenditure_record":
                try: insert_expenditure_record(**arguments_dict)
                except Exception as e: print(e)
    return ittem_counts

if __name__ == '__main__':
    messages = []
    messages.append({"role": "system", "content": "You will extract the purchase information from the user prompt and call the insert_expenditure_record function to insert record into the expenditure_table one by one. You will do this job in just one prompt, so don't ask user for any clarification. Put 0 or None for the fields that are not available. If you find no date and time infor, please use current time for the date and time (no need for seconds info) fields."})
    messages.append({"role": "user", "content":'''
    This image shows a shopping receipt with a list of items purchased, their prices, and the total amount. The items listed on the receipt are:

    - FLORIDAS NATURAL (2 entries, with member savings of -$0.49 each), priced at $2.99 each, with the final price being $2.50 each after savings.
    - LUCERNE WHOLE MILK, priced at $4.99.
    - BLUEBERRIES ORGNC, priced at $8.99.
    - GALA APPLES LARGE, with a weight of 3.96 pounds at a unit price of $2.69 per pound, totaling $10.65.
    - GRAPE RD SDLSS ORG (presumably organic red seedless grapes), with a weight of 2.24 pounds at a unit price of $4.99 per pound, totaling $11.18.

    The tax appears to be $0.00, with a total balance due of $91.01.'''})

    assistant_message = run_gpt_with_function_calls(messages)
