#!/usr/bin/env python
# coding: utf-8
# created on pancake by firened
import subprocess
import threading

import os
import random
import discord

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')

updateID = 0
voltage = 0

client = discord.Client()

def measure():
    t = threading.Timer(30.0, measure)
    t.daemon = True
    t.start()
    
    global updateID
    global voltage

    # get voltage
    string_before_cleaning_and_decoding =  subprocess.Popen("sudo i2cget -y 1 0x62 0x02 w", shell=True, stdout=subprocess.PIPE).stdout
    string_before_cleaning = string_before_cleaning_and_decoding.read()

    # cleanup measurement
    string = string_before_cleaning[2:]
    number_raw_volts = int(string, 16)
    number_volts = ((number_raw_volts & 0xFF00) >> 8) | ((number_raw_volts & 0x00FF) << 8)
    uV_volts = number_volts * 305
    voltage = uV_volts / 1000

    updateID += 1

    # output the voltage
    print(str(voltage) + "mV")
    #if not client.is_closed():
    #    channel = client.get_channel(864879333428559898)
    #    channel.send('hello')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


#@bot.command(name='status', help='Responds with battery status')
#async def status(ctx):
#    response = str(voltage) + "mV"
#    await ctx.send(response)

#start interval timer thread
measure()

client.run(TOKEN)


