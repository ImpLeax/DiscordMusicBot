import disnake
import logging
import os
from dotenv import load_dotenv
from os import getenv
from disnake.ext import commands

load_dotenv()
TOKEN = getenv('token')
bot = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all())


for filename in os.listdir("./commands"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"commands.{filename[:-3]}")


@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Game(name="on гофрошка"), status=disnake.Status.online)
    print(f"Bot {bot.user} is on!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Error {e}")
        input("Press enter to exit...")