import discord
import os
import sys
from dotenv import load_dotenv
from triviabot import FindAnswers

client = discord.Client()
fa = FindAnswers()
load_dotenv()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send("Hello! I'm a trivia bot that tries to answer questions based on wikipedia. To find out more please type $help")
    elif message.content.startswith('$trivia'):
        question = message.content.split('$trivia ')[-1]
        try:
            answer = fa.AnswerQuestion(question)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            answer = "I'm sorry i couldnt answer that"
        await message.channel.send(answer)
    elif message.content.startswith('$help'):
        await message.channel.send("to as a question e.g. 'What is the meaning of life?' please type '$trivia What is the meaning of life?'")

client.run(os.getenv('TOKEN'))