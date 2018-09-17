import discord
import youtube_dl
from discord.ext import commands
from discord.voice_client import VoiceClient


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



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

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        if ctx.voice_client is None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(pass_context=True)
    async def leave(ctx):
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        await self.voice_client.disconnect()

    @commands.command(name='play')
    async def cog_play(self, ctx, url):
        #voice_client = await ctx.message.author.voice.channel.connect()
        #player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            self.players[ctx.guild.id] = player
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now Playing: {}'.format(player.title))

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

    @cog_play.before_invoke
#    @yt.before_invoke
#    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client_is_playing():
            ctx.voice_client.stop()

def setup(client):
    client.add_cog(Music(client))
