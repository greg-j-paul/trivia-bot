# TRIVIA bot

A little project to answer trivia questions with off the shelf components.
Given a question it will:
1. Use extract named entites
2. Find wiki pages for these entities
3. Attempt to use huggingface question answering pipeline to find the answers.
4. Connect to discord server


# TO RUN:
Please install requirements as per `requirements.txt` and either run `notebooks\triviabot.ipynb` or start the bot.

To start the bot:
1. Please follow [instructions](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) to add the bot account
2. Create a .env file with the `TOKEN=whateveryourtokenis`
3. Run `python main.py`

