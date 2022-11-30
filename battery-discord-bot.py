#!/usr/bin/env python
# coding: utf-8
# created on pancake by firened
import subprocess
import socket
import threading

import os
import random

from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')

updateID = 0
voltage = 0

bot = commands.Bot(command_prefix='!')

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


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the ðemoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='status', help='Responds with battery status')
async def status(ctx):

    response = str(voltage) + "mV"
    await ctx.send(response)

#start interval timer thread
measure()

bot.run(TOKEN)


