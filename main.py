import disnake
from disnake.ext import commands
from save_load import *

bot = commands.Bot(command_prefix="*")


@bot.slash_command(name="personagens", description="Veja seus personagens, da pessoa mencionada ou de algum UID específico.")
async def personagens(context, usuario : disnake.User = None, uid : int = None):
    await context.channel.send("salve")


@bot.slash_command(name="registrar", description="Registre seu uid ")
async def registrar(context, uid : int):
    await context.channel.send("salve")


tokenBot = carregar("keys")["discord"]
bot.run(tokenBot)
