from disnake.ext import commands

class PauseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pause')
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Music playback paused.")
        else:
            await ctx.send("Nothing is currently playing!")

def setup(bot):
    bot.add_cog(PauseCommand(bot))