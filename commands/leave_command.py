from disnake.ext import commands

class LeaveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leave')
    async def leave(sefl, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None or not ctx.voice_client.is_connected():
                pass
            else:
                await ctx.voice_client.disconnect()
                await ctx.send(f"Disconnected from {channel}!")
        else:
            await ctx.send("Join to voice channel first!!!")

def setup(bot):
    bot.add_cog(LeaveCommand(bot))