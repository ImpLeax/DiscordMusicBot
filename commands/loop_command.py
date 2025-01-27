from disnake.ext import commands

class LoopState:
    looped = False

class LoopComm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='loop')
    async def loop(self, ctx):
        LoopState.looped = not LoopState.looped  
        print(f"Loope status:{LoopState.looped}")
        if LoopState.looped:
            status = 'enabled'
        else:
            ctx.voice_client.stop()
            status = 'disabled'
        await ctx.send(f"Looping has been {status}.")


def setup(bot):
    bot.add_cog(LoopComm(bot))