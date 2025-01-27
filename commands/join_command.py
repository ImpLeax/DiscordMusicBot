import disnake
from disnake.ext import commands

class JoinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='join')
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None or not ctx.voice_client.is_connected():
                await channel.connect(reconnect=False)
                await ctx.send(f"Connected to {channel}!")
            else:
                await ctx.send("Already connected to voice channel!")
        else:
            await ctx.send("Join to anyone voice channel first!!!")

def setup(bot):
    bot.add_cog(JoinCommand(bot))