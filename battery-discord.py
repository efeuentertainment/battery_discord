#!/usr/bin/env python
# coding: utf-8
# created on pancake by firened
import subprocess
#import threading
import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
USER_ID = os.getenv('USER_ID')

updateID = 0
voltage = 0
lowVoltageAlarm = 3400
lowVoltageSentFlag = True
customVoltageAlarm = 4300
customVoltageSentFlag = False

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # an attribute we can access from our task
    self.counter = 0

    # start the task to run in the background
    self.my_background_task.start()

  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
  async def on_message(self, message):
    # we do not want the bot to reply to itself
    if message.author.id == self.user.id:
      return

    if message.content.startswith('!status'):
      #response = f'{message.author.mention} ' + str(voltage) + " mV"
      response = str(voltage) + " mV"
      print(response)
      await message.reply(response, mention_author=False)
  
  #@client.event
#  async def on_message(message):
#    if message.author == client.user:
#      return
#
#    if message.content == '!status':
#        response = str(voltage) + "mV"
#        await message.author.send('hi')
#        await message.channel.send(response)
#    elif message.content == '!raise-exception':
#        raise discord.DiscordException


  @tasks.loop(seconds=10)  # task runs every 60 seconds
  async def my_background_task(self):

    global updateID
    global voltage
    global lowVoltageAlarm
    global lowVoltageSentFlag
    global customVoltageAlarm
    global customVoltageSentFlag

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
#    print(str(voltage) + "mV")
#    print('sending')
#    channel = self.get_channel(864879333428559898)  # channel ID goes here
#    self.counter += 1
#    await channel.send(str(voltage) + "mV")
    
    #low voltage alarm
    if voltage < lowVoltageAlarm and not lowVoltageSentFlag:
      lowVoltageSentFlag = True
      msg = f"<@{USER_ID}> " + "low voltage:\n"
      msg += str(voltage) + " mV"
      print(msg)
      channel = self.get_channel((int)(CHANNEL_ID))  # channel ID goes here
      await channel.send(msg)

    if voltage > (lowVoltageAlarm + 200):
      lowVoltageSentFlag = False

    #custom voltage alarm
    if voltage < customVoltageAlarm and not customVoltageSentFlag:
      customVoltageSentFlag = True
      msg = f"<@{USER_ID}> " + "below custom voltage:\n"
      msg += str(voltage) + " mV"
      print(msg)
#      print(CHANNEL_ID)
#      print(864879333428559898)
      channel = self.get_channel((int)(CHANNEL_ID))  # channel ID goes here
      await channel.send(msg)

    if voltage > (customVoltageAlarm + 200):
      lowVoltageSentFlag = False


  @my_background_task.before_loop
  async def before_my_task(self):
    #print('connecting')
    await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
