# Telegram Assistant

This project is a Telegram bot that uses OpenAI's GPT-3 model to interact with users. It can handle various commands and can even translate messages into different languages.

## Features

- Start and stop listening to a chat.
- Rewrite a message using GPT-3.
- Write a new message using GPT-3.
- Translate a message into English, Russian, German, or French.
- Respond to regular messages using GPT-3.

## Setup
You will need to obtain the following:
    - `api_id` and `api_hash` from Telegram. You can get these by creating a new application on the [Telegram website](https://my.telegram.org/apps).
    - `openai_api_key` from OpenAI. You can get this by registering on the [OpenAI website](https://beta.openai.com/signup/).
    
1. Clone this repository.
2. Install the required Python packages: `pip install -r requirements.txt`
3. Modify a `config.json` file in the root directory with your data.
4. Run the script: `python assistant.py`.

## Usage

- Send `!start` to start the bot listening to a chat.
- Send `!stop` to stop the bot listening to a chat.
- Reply to a message with `!rewrite {prompt}` to rewrite the message using GPT-3.
- Send `!write {message}` to write a new message using GPT-3.
- Send `{language_command} {message}` to translate the message into the specified language. The language commands are `!eng` for English, `!rus` for Russian, `!ger` for German, and `!fr` for French.
- You can add your own language for translation by changing `language_abbreviations` in file `config.json`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
