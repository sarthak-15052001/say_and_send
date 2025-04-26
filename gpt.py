import os
import re
from dotenv import load_dotenv
import requests

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


openai_url = "https://api.openai.com/v1/chat/completions"               # OpenAI API endpoint URL




def chatGpt(query_prompt):
    try:
        model = "gpt-3.5-turbo"                               # model to be used for generating the chat completion.
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",      # adds the API key for authentication. 
            "Content-Type": "application/json",               # specifies that the request body will be in JSON format.
        }
        data = {                                        # Here data contains the payload for POST requests
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates email subjects in Hebrew.",
                },                                        #  Adds a dictionary to the messages list. This dictionary sets the system message, establishing the assistant's role.
                {
                    "role": "user",
                    "content": query_prompt,              #  Adds a dictionary to the messages list. This dictionary sets the user message, using the query_prompt parameter as the content.
                },
            ],
            "max_tokens": 1024,                           # Limits the maximum number of tokens in the generated response to 1024.
        }

        response = requests.post(openai_url, headers=headers, json=data)

        if response.status_code == 200:
            chat_completion = response.json()
            chat = chat_completion["choices"][0]["message"]["content"].strip()     # Extracts the content of the first choice's message from the chat_completion object and assigns it to the variable chat. becz response may include multiple choices, but only the first one's message content is being used here.
            return chat
        else:
            return {"error": response.text}

    except Exception as e:
        return {"error": str(e)}
    

def generate_subject(input_text):
    if not input_text:                          # checks whether input_text variable is empty or none
        return None                             # The return statement exits the function early if no input was provided, preventing further execution.

    try:
        # Generate the query prompt
        query_prompt = f"Based on the provided input text in Hebrew, please generate an email subject in Hebrew. No additional data is needed; just provide the email subject:.\n\n{input_text}"

        # Call the chatGpt function
        subject = chatGpt(query_prompt).strip()             # strip() method is called on the result to remove any leading or trailing whitespace.

        # Remove flags using regular expressions
        subject = re.sub(r'[\U0001F1E6-\U0001F1FF]{2}', '', subject)      # The function uses a regular expression to remove any flag emojis from the subject


        # Return the generated subject in a response message
        return {"subject": subject, "message": "Subject generated successfully"}
    except Exception as e:
        # print({'error': str(e)})
        return {"error": str(e)}