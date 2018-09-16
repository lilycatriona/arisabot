import discord
import youtube_dl
from discord.ext import commands
from discord.voice_client import VoiceClient

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.queues = {}

    def voice_client(self, server):
        return self.bot.voice_client_in(server)

    def voice_connected(self, server):
        if self.bot.is_voice_connected(server):
            return True

    def check_queue(id):
        if queues[id] != []:
            player = queues[id].pop(0)
            players[id] = player
            player.start()

    async def on_message_delete(self, message):
        await self.send('Message Deleted')

    @commands.command(pass_context=True)
    async def join(ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.join_voice_channel(channel)

    @commands.command(pass_context=True)
    async def leave(ctx):
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        await self.voice_client.disconnect()

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        server = ctx.message.server
        voice_client = self.voice_client(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        players[server.id] = player
        player.start()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        id = ctx.message.server.id
        players[id].pause()

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        id = ctx.message.server.id
        players[id].stop()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        id = ctx.message.server.id
        players[id].resume()

    @commands.command(pass_context=True)
    async def queue(self, server, url):
        voice_client = self.voice_client(server)
        print(self.voice_client(server))
        #bot.voice = self.bot.voice_client_in(server)
        print(self.voice_client)
        self.player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await client.say("Queued Video")

def setup(client):
    client.add_cog(Music(client))
