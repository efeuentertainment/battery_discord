import discord
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        print('sending')
        counter = 0
        channel = self.get_channel(864879333428559898)  # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(5)  # task runs every 60 seconds


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
