from Top_functions import *

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

'''
curl https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$API_KEY \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{
          "text": "Write a story about a magic backpack."}]}]}' 2> /dev/null'''

# define a function to use requests to generate text from googleapis
def generate_text(prompt, model_name='gemini-pro'):
    print(f"CALLING generate_text() to generate text answer for prompt: {prompt}...")
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    data = {'contents': [{'parts': [{'text': prompt}]}]}
    response = requests.post(url, headers=headers, json=data)
    # print(json.dumps(response.json(), indent=2))
    '''{"candidates": [
        {
        "content": {
            "parts": [
            {
                "text": "The meaning of life is a question that has occupied the minds of philosophers, theologians, scientists, and artists for centuries. Despite being an age-old question, there is no definitive answer applicable to everyone. The pursuit of understanding the meaning of life is a highly personal and subjective journey, varying across individuals, cultures, and belief systems. Here are some prevalent perspectives on the meaning of life:\n\n1. **Purpose-Driven Meaning:** Some believe that life's meaning stems from discovering and fulfilling a specific purpose or set of goals. This purpose can be related to one's career, relationships, creative endeavors, or making a positive impact in the world.\n\n2. **Eudaimonia and Happiness:** The ancient Greek concept of eudaimonia refers to a state of well-being or human flourishing. Many people find meaning in life by striving to achieve happiness, contentment, and fulfillment in their personal lives and relationships.\n\n3. **Existential Meaning-Making:** Existentialists believe that meaning is not inherent in life but must be actively created by each individual. This involves making conscious choices, assuming responsibility for one's existence, and embracing freedom to shape one's life.\n\n4. **Religious and Spiritual Meaning:** For many, the meaning of life is deeply intertwined with religious or spiritual beliefs. They find purpose and fulfillment in connecting with a higher power, following religious teachings, or exploring spiritual practices.\n\n5. **Contributive Meaning:** Some individuals find meaning in making a positive contribution to society or the world around them. This can involve acts of kindness, volunteering, philanthropy, or working towards social justice or environmental causes.\n\n6. **Experiential Meaning:** Others find meaning in the simple but profound experiences of life. This can include appreciating the beauty of nature, savoring moments of joy, connecting with loved ones, or pursuing hobbies and interests that bring fulfillment.\n\n7. **Self-Actualization:** Humanistic psychologists like Abraham Maslow believed that self-actualization, or realizing one's full potential, is the ultimate goal of life. This often involves personal growth, self-discovery, and living in accordance with one's values.\n\n8. **Legacy and Impact:** Some find meaning in creating a lasting legacy or impact that extends beyond their lifetime. This can involve leaving a mark through creative works, raising a family, mentoring others, or contributing to a cause that will continue to affect future generations.\n\nUltimately, the meaning of life is a deeply personal and unique quest that each individual must explore and define for themselves. There is no right or wrong answer, and the meaning may evolve and change over time as one's experiences, values, and priorities shift."
            }
            ],
            "role": "model"
        },
        "finishReason": "STOP",
        "index": 0,
        "safetyRatings": [
            {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "probability": "NEGLIGIBLE"
            },
            {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "probability": "NEGLIGIBLE"
            },
            {
            "category": "HARM_CATEGORY_HARASSMENT",
            "probability": "NEGLIGIBLE"
            },
            {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "probability": "NEGLIGIBLE"
            }
        ]
        }
    ],
    "promptFeedback": {
        "safetyRatings": [
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "probability": "NEGLIGIBLE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "probability": "NEGLIGIBLE"
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "probability": "NEGLIGIBLE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "probability": "NEGLIGIBLE"
        }
        ]
    }
    }
    '''
    response_text = response.json()['candidates'][0]['content']['parts'][0]['text']
    print(f"GEMINI API RESPONSE TEXT: \n\n{response_text}\n\n")
    return response_text


# get the response text from generate_text function and send back to the user
def gemini_gpt(prompt, from_id=TG_BOT_OWNER_ID):
    print("CALLING GEMINI GPT to generate text answer...")
    try: send_msg(generate_text(prompt), from_id)
    except: return


if __name__ == '__main__':
    response_text = generate_text("when was google founded")
    print(response_text)