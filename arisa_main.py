import discord
import youtube_dl
import os
import yaml
from discord.ext import commands
from discord.voice_client import VoiceClient

def get_prefix(bot, message):
    prefixes = ['.']
    return commands.when_mentioned_or(*prefixes)(bot, message)

extensions = ["arisa_music", "arisa_owner"]

with open('config.yml') as config:
    doc = yaml.load(config)
    TOKEN = doc["token"]
bot = commands.Bot(command_prefix=get_prefix)

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load Extension {}\n{}'.format(extension, exc))

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Succesfully Started')


bot.run(TOKEN)
