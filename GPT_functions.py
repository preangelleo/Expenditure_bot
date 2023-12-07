from openai import OpenAI
from dotenv import load_dotenv
import os

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

'''
assistant = client.beta.assistants.create(
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4-1106-preview",
  tools=[{
      "type": "function",
    "function": {
      "name": "getCurrentWeather",
      "description": "Get the weather in location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
          "unit": {"type": "string", "enum": ["c", "f"]}
        },
        "required": ["location"]
      }
    }
  }, {
    "type": "function",
    "function": {
      "name": "getNickname",
      "description": "Get the nickname of a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
        },
        "required": ["location"]
      }
    } 
  }]
)
'''
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

# define GPT Assistant with code_interpreter type
def ask_gpt_assistant_coding(assistant_name, system_prompt, point_model="gpt-4-1106-preview"):
    response = client.beta.assistants.create(
        name=assistant_name,
        instructions=system_prompt,
        tools=[{"type": "code_interpreter"}],
        model=point_model
    )
    return response
'''Assistant(id='asst_EGt7Zi9QI88PsY6OHQG1W9nl', created_at=1701933888, description=None, file_ids=[], instructions='You are a personal math tutor. Write and run code to answer math questions.', metadata={}, model='gpt-4-1106-preview', name='Math Tutor', object='assistant', tools=[ToolCodeInterpreter(type='code_interpreter')])'''


# assistant_response = ask_gpt_assistant_coding("Math Tutor", "You are a personal math tutor. Write and run code to answer math questions.")
# print(assistant_response)

thread = client.beta.threads.create()
'''Thread(id='thread_9kyOVd4uOkmBzP7E4Yu84Xnf', created_at=1701934168, metadata={}, object='thread')
thread_9kyOVd4uOkmBzP7E4Yu84Xn'''
# print(thread)
# print(thread.id)

