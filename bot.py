import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
bot = commands.Bot(command_prefix="!", description='Scrapping bot')
TOKEN = "REDACTED"

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
@has_permissions(administrator=True)
@bot.command()
async def reload(ctx):
    """Reloads a module."""
    try:
        bot.unload_extension("headless")
        bot.load_extension("headless")
    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send('\N{OK HAND SIGN}')
bot.run(TOKEN, bot=True, reconnect=True)

