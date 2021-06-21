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

intents = discord.Intents.default()
intents.members = True

class algorithmic_bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.role_message_id = 856358629804736512
        self.emoji_to_role = {
            discord.PartialEmoji(name='🔴'): 856360034221293578,
            discord.PartialEmoji(name='🟡'): 844969982261067786,
            discord.PartialEmoji(name='green', id=0): 844970072112103445
        }

    @client.event
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))
    
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        # except discord.HTTPException:
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            await payload.member.add_roles(role)
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    @client.event
    async def on_message(self, message):
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
            await message.channel.send('```Guess a number between 1 and 10. (timeout is 10 seconds)```')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await client.wait_for('message', check=is_correct, timeout=10.0)
            except asyncio.TimeoutError:
                return await message.channel.send('```Sorry, you took too long it was {}.```'.format(answer))

            if int(guess.content) == answer:
                await message.channel.send('```You are right!```')
            else:
                await message.channel.send('```Oops. It is actually {}.```'.format(answer))

client = algorithmic_bot(intents=intents)
client.run(Token)
