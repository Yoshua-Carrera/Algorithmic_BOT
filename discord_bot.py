import discord
import os
from replit import db
import json
import random
import asyncio
from pathlib import Path

token_path = 'env'
token_file = '/variables.json'

try:
    with open(token_path+token_file, 'r') as tkn:
        Token = json.load(tkn)[0]['Token']
except:
    data =[{"Token": "ADD YOUR TOKEN HERE"}]

    Path(token_path).mkdir(parents=True, exist_ok=True)
    with open(token_path+token_file, 'w') as tkn:
        json.dump(data, tkn)

    print('Please add your token inside of {}'.format(token_path+token_file))
    exit()

client = discord.Client()
key_char = '.'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    
    if message.content.startswith('{}hello'.format(key_char)):
        await message.channel.send('```hello```')
    
    if message.content.startswith('{}jianing'.format(key_char)):
        await message.channel.send('```hello Jianing```')
    
    if message.content.startswith('{}ping'.format(key_char)):
        ping = msg.split("$ping ",1)[1]
        await message.channel.send('{} {}'.format(ping, 'has been pinged'))
    
    if message.content.startswith('{}guess'.format(key_char)):
        await message.channel.send('```Guess a number between 1 and 10.```')

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await client.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send('```Sorry, you took too long it was {}.```'.format(answer))

        if int(guess.content) == answer:
            await message.channel.send('```You are right!```')
        else:
            await message.channel.send('```Oops. It is actually {}.```'.format(answer))

client.run(Token)