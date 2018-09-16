import discord
import youtube_dl
from discord.ext import commands
from discord.voice_client import VoiceClient

extensions = ["arisa_music"]
bot = commands.Bot(".")
TOKEN = 'changethis'

bot = discord.Client()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'))

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)
    await bot.process_commands(message)
@bot.command()
async def ping():
    await bot.say("Pong")

@bot.command()
async def die(self):
    await bot.say(message.channel, 'Shutting Down')
    await bot.close()

@bot.command()
async def load(extension):
    try:
        bot.load_extension(extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))

@bot.command()
async def unload(extension):
    try:
        bot.unload_extension(extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load Extension {}\n{}'.format(extension, exc))

bot.run(TOKEN)
