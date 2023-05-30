from pyrogram import Client, filters
import openai
import logging
import json

# Load configuration data from JSON file
with open('config.json') as config_file:
    config_data = json.load(config_file)

openai.api_key = config_data['openai_api_key']
api_id = config_data['telegram_api_id']
api_hash = config_data['telegram_api_hash']
my_user_id = config_data['my_user_id']
LANGUAGE_ABBREVIATIONS = config_data['language_abbreviations']
phone = config_data['phone_numb']
logging.basicConfig(level=logging.INFO)

class TelegramAssistant:
    def __init__(self, phone):
        self.dialogues = {}
        self.phone = phone
        self.client = Client(name=self.phone, api_id=api_id, api_hash=api_hash, phone_number=self.phone)
        self.client.on_message(filters.text)(self.handle)

    def handle(self, client, message):
        chat_id = message.chat.id
        user_id = message.from_user.id  # Get User ID of the message sender

        MY_USER_ID = my_user_id

        # Check if the message starts with !start or !stop
        if user_id == MY_USER_ID:  # Check if the sender is you
            if message.text.startswith('!start'):
                if chat_id not in self.dialogues:
                    self.dialogues[chat_id] = [
                        {"role": "system", "content": "You are a helpful assistant."},
                    ]
                    print("Started listening to this chat.")
                # Delete the message with the !start command
                message.delete()

            elif message.text.startswith('!stop'):
                if chat_id in self.dialogues:
                    del self.dialogues[chat_id]
                    print("Stopped listening to this chat.")
                # Delete the message with the !stop command
                message.delete()

            elif message.text.startswith('!rewrite') and message.reply_to_message:
                # Get the text of the message we are replying to
                reply_message = message.reply_to_message.text
                print('Reply message: ', reply_message)
                
                # Get the prompt from the message
                prompt = message.text[9:]  # Take everything after !rewrite or !write
                print('Prompt: ', prompt)

                # Send text to ChatGPT via API
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": reply_message},
                    ]
                )

                # Edit the message we are replying to with new text
                message.reply_to_message.edit_text(response['choices'][0]['message']['content'])
                
                # Delete the message with the !rewrite command
                message.delete()

            elif message.text.startswith('!write'):
                # Get the prompt from the message
                prompt = message.text[7:]  # Take everything after !write
                print('Prompt: ', prompt)

                # Send text to ChatGPT via API
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ]
                )

                # Edit the message with the !write command with new text
                message.edit_text(response['choices'][0]['message']['content'])

            elif any(message.text.startswith(command) for command in LANGUAGE_ABBREVIATIONS):
                first_word = message.text.split(" ")[0]  # Extract the first word from the message```python
                # Get the prompt from the message
                prompt = message.text[len(first_word) + 1:]  # Take everything after "{first_word} "
                print('Prompt: ', prompt)

                # Create a system message using the full name of the language
                system_message = f"Literally translate the following message into {LANGUAGE_ABBREVIATIONS[first_word]}"

                # Send text to ChatGPT via API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt},
                    ]
                )

                # Edit the message with the {first_word} command with new text
                message.edit_text(response['choices'][0]['message']['content'])

        # Handling regular messages
        elif chat_id in self.dialogues:
            print(f"Received message: {message.text}")
            # Add a new user message to the dialogue history
            self.dialogues[chat_id].append({"role": "user", "content": message.text})

            model_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.dialogues[chat_id]
            )

            response = model_response['choices'][0]['message']['content']

            # Add the model's response to the dialogue history
            self.dialogues[chat_id].append({"role": "assistant", "content": response})

            print(f"Responding with: {response}")
            message.reply(response)

            # If the dialogue history becomes too large, remove the oldest messages
            if len(self.dialogues[chat_id]) > 6:  # Prompt + 5 last message exchanges
                del self.dialogues[chat_id][1]  # Delete the second element in the list, leaving the prompt untouched

    def start(self):
        self.client.run()

if __name__ == "__main__":
    assistant = TelegramAssistant(phone=phone)
    assistant.start()       
