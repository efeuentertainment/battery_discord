import os
from discord.ext import tasks
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')

import discord


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

#    async def setup_hook(self) -> None:
        print('hook')
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=5)  # task runs every 60 seconds
    async def my_background_task(self):
        print('sending')
        channel = self.get_channel(864879333428559898)  # channel ID goes here
        self.counter += 1
        await channel.send(self.counter)

    @my_background_task.before_loop
    async def before_my_task(self):
        #print('before')
        print('waiting')
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
