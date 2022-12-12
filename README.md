## battery_discord
standalone discord bot to observe 1S battery voltage using i2c CW2015 IC. often used in 1S Raspberry Pi UPS hats. can be used for robots, etc.
- sends a notification when voltage drops below thresholds.
- replies with current voltage to `!status` command.

## Install:
```
sudo apt update
sudo apt install pip python3
sudo python3 -m pip install -U python-dotenv
```
clone this github repo to your device.

add a discord app, bot (and maybe guild) according to https://realpython.com/how-to-make-a-discord-bot-python/

insert your bot token, channel_id and user_id into .env :
```
sudo mv .env-blank .env
sudo nano .env
```
run it:
```
python3 battery-discord.py
```

### Based on code and examples from:
https://discordpy.readthedocs.io/en/stable/#getting-started
https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
https://github.com/SebbyLaw/discord.py/blob/a116d568dc3c751801c5fa00387bc0edb664aadb/examples/background_task.py
https://realpython.com/how-to-make-a-discord-bot-python/
