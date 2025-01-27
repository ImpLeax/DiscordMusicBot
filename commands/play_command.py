from .cfg.source import YTDLSource
import logging
import asyncio
from .cfg.options import *
from .loop_command import LoopState
import random
import disnake
import yt_dlp
from disnake.ext import commands
from .buttons.buttons import PlaybackControls


class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disconnecting = False
        self.queue = []
        self.current = None
        self.current_url = None

    async def _handle_after_play(self, ctx, error):
        if LoopState.looped:
            self.queue.insert(0, self.current_url)
        await self.play_next(ctx)

    async def get_audio_url(self, video_url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info['url']

    async def get_object(self, search_query):
        return await YTDLSource.from_query(search_query)

    async def safe_disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            self.queue.clear()
            self.current = None
            logging.info("Bot disconnected safely.")

    async def play_music(self, ctx, search_query):
        async with ctx.typing():
            try:
                player = await self.get_object(search_query)
                self.current_url = await self.get_object(search_query)
                self.queue.append(player)

                await ctx.send(f"Added to queue: **{player.title}**")
                await ctx.send(f"⌚ Loading... **{player.url}**")

                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)
            except Exception as e:
                logging.error(f"Failed to play the audio: {e}")
                await ctx.send(f"Failed to play the audio: {e}")

    async def play_next(self, ctx):
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            await ctx.send("I'm not connected to any voice channel.")
            return

        if self.queue:
            player = self.queue.pop(0)


            try:
                audio_url = self.current if LoopState.looped and self.current is not None else await self.get_audio_url(player.url)
                self.current = None if LoopState.looped else await self.get_audio_url(player.url)
                ffmpeg_options = ffmpeg_looped if LoopState.looped else ffmpeg_standart
                audio_source = disnake.FFmpegPCMAudio(audio_url, **ffmpeg_options)

                ctx.voice_client.play(
                    audio_source,
                    after=lambda e: asyncio.run_coroutine_threadsafe(self._handle_after_play(ctx, e), self.bot.loop)
                )
                view = PlaybackControls(ctx, self)
                await ctx.send(f"Now playing: **{player.title}**", view=view) if not LoopState.looped or not ctx.voice_client.is_playing() else None
            except Exception as e:
                logging.error(f"Error during playback: {e}")
                await ctx.send("An error occurred while playing the track.")
                await self.safe_disconnect(ctx)
        else:
            await ctx.send("Queue finished!")

    @commands.command(name="play")
    async def play(self, ctx, *query):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None or not ctx.voice_client.is_connected():
                await channel.connect()
                await ctx.send(f"Connected to {channel}!")

            await self.play_music(ctx, " ".join(query))
        else:
            await ctx.send("Join a voice channel first!")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.disconnecting:
            return

        voice_client = member.guild.voice_client

        if not voice_client:
            return

        if before.channel is not None and after.channel is None and member == self.bot.user:
            logging.info(f"Bot was forcibly disconnected from {before.channel.name}.")
            self.disconnecting = True
            try:
                if len(before.channel.members) == 1:
                    await voice_client.disconnect(force=True)
                    self.queue.clear()
                    self.current = None
                    logging.info("Bot disconnected due to inactivity.")
            except Exception as e:
                logging.error(f"Error during forced disconnection: {e}")
            finally:
                self.disconnecting = False

        if len(voice_client.channel.members) == 1 and voice_client.channel.members[0] == self.bot.user:
            await asyncio.sleep(10)
            if len(voice_client.channel.members) == 1:
                if not self.current and not voice_client.is_playing():
                    self.disconnecting = True
                    try:
                        await voice_client.disconnect(force=True)
                        self.queue.clear()
                        self.current = None
                        logging.info("Bot disconnected due to inactivity.")
                    except Exception as e:
                        logging.error(f"Error during disconnection due to inactivity: {e}")
                    finally:
                        self.disconnecting = False

    @commands.command(name="queue")
    async def queue_cmd(self, ctx):
        if self.queue:
            queue_list = "\n".join(f"**{i+1}.** {track.title}" for i, track in enumerate(self.queue))
            await ctx.send(f"**Queue:**\n{queue_list}")
        else:
            await ctx.send("Queue is empty.")

    @commands.command(name="shuffle")
    async def shuffle(self, ctx):
        random.shuffle(self.queue)
        await ctx.send("The queue has been shuffled!")

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current track.")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.voice_client:
            LoopState.looped = False
            self.queue.clear()
            ctx.voice_client.stop()
            await ctx.send("Stopped playback and cleared the queue.")
        else:
            await ctx.send("I'm not connected to any voice channel.")

def setup(bot):
    bot.add_cog(PlayCommand(bot))