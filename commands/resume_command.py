from disnake.ext import commands

class ResumeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='resume')
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed playback.")
        else:
            await ctx.send("Nothing is paused!")

def setup(bot):
    bot.add_cog(ResumeCommand(bot))