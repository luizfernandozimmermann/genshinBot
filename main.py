from datetime import datetime
import disnake
from disnake.ext import commands

from outros.save_load import *
from outros.ImagemPersonagens import *


intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.load_extensions("comandos")


@bot.event
async def on_slash_command_error(inter : disnake.ApplicationCommandInteraction, 
                                 exception : commands.CommandError):
    try:
        await inter.response.defer()
    except:
        pass
    
    await bot.owner.send(f"## Ocorreu um erro: " +
                            f"\n- Servidor: **{inter.guild.name}**" +
                            f"\n- Canal: **{inter.channel.name}** às **{datetime.now().strftime('%H:%M:%S, %Y/%m/%d')}**" + 
                            f"\n- Usuário: **{inter.user.name}**" + 
                            f"\n- Comando: **{inter.application_command.name}**" +
                            f"\n- Exceção: \n```{exception}```")
    
    await inter.edit_original_message("Ocorreu um erro :(. O erro foi reportado.")


chaves = carregar("keys")
tokenBot = chaves["discord"]
bot.run(tokenBot)
