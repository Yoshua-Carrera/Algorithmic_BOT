import discord
import os
from replit import db
import json

with open('env/variables.json', 'r') as tkn:
    Token = json.load(tkn)[0]['Token']

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('hello')

client.run(Token)