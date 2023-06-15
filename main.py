import discord
import time
import install
from discord.ext import commands
import youtube_dl
import asyncio

#import logging

#logging.basicConfig(level=logging.DEBUG)

"""

audiobot\Lib\site-packages\youtube_dl\extractor\youtube.py

copy the below line and replace line 1794

'uploader_id': self._search_regex(r'/(?:channel/|user/|@)([^/?&#]+)', owner_profile_url, 'uploader id', default=None),

"""

install.install() # downloads ffmpeg

runningOnPi = 1 #depending on the python version it needs the full path. on my main pc and the pi, it works with just the file name, but my laptop needs the full path. set to one for rapid debugging
#runningOnPi = int(input('Is this running on the pi? 1 for yes 0 for no.'))
if runningOnPi == 1:
    x = open("data.env", 'rt')
else:
    x = open("Python/Yet Another Audio Bot/data.env", 'rt')
dotenv = x.readlines(0)
discordToken = dotenv[0]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

global vc
global channel

ytdl_format_options = {
    'format': 'worstaudio/worst',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    '-list-formats': True,
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'options': '-vn',
}

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
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("$"),
    description='Relatively simple music bot example',
    intents=intents,
)


class sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await ctx.guild.change_voice_state(channel=channel, self_deaf=True)

        await channel.connect()
    
    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            
        await ctx.send(f'Now playing: {player.title}')
        
    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def noot(self,ctx):
        """noot"""
        channel = ctx.author.voice.channel
        vc = ctx.guild.voice_client
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source='skullsound3.mp3'))
        #while vc.is_playing():
        #    time.sleep(0.1)

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    @noot.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

@client.event
async def on_message(message):

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$1noot'):
        channel = message.author.voice.channel
        vc = message.guild.voice_client
        vc.play(discord.FFmpegPCMAudio(source='skullsound3.mp3'))
        #while vc.is_playing():
        #    time.sleep(0.1)

    if message.content.startswith('$connect'):
        # Check if author is in a voice channel
        if message.author.voice:
            channel = message.author.voice.channel
            vc = await channel.connect()
        else:
            await message.channel.send("You need to be in a voice channel first.")
        await vc.guild.change_voice_state(channel=channel, self_deaf=True)

    if message.content.startswith('$disconnect'):
        # Get voice client for guild
        vc = message.guild.voice_client

        # Check if voice client is connected
        if vc:
            # Disconnect from voice channel
            await vc.disconnect()
        else:
            await message.channel.send("I am not connected to a voice channel.")



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

async def main():
    async with bot:        
        await bot.add_cog(sounds(bot))
        await bot.start(f'{discordToken}')

asyncio.run(main())