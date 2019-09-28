import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions, CheckFailure

bot = commands.Bot(command_prefix="!", description='Scrapping bot')
TOKEN = "NjE0NDM3NDA0NDYzNDY0NDQ5.XV_dmQ.SOoYlPaJmQ8NUfhBENtp5c3Ru9g"

if __name__ == '__main__':
    bot.load_extension("headless")
@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')
@bot.command()
@has_permissions(administrator=True)
async def quit(ctx):
    await bot.logout()

bot.run(TOKEN, bot=True, reconnect=True)

