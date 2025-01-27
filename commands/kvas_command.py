from disnake.ext import commands

class KvassComm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kvas')
    async def kvas(self, ctx):
        await ctx.send("Максим Квас Чепух!")


def setup(bot):
    bot.add_cog(KvassComm(bot))
