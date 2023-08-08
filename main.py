import disnake
from disnake.ext import commands

import genshinstats as gs

from save_load import *
from imagem import *


bot = commands.Bot(command_prefix="*")

@bot.slash_command(name="personagens", description="Veja seus personagens, da pessoa mencionada ou de algum UID específico.")
async def personagens(inter, usuario : disnake.User = None, uid : int = None):
    idAutor = inter.author.id

    if uid == None:
        if usuario == None:
            if f"{idAutor}" not in usuarios:
                await inter.response.send_message("Registre seu uid ou utilize o seu UID como parâmetro.")
                return
        
            uid = usuarios[f"{idAutor}"]

        else:
            if f"{usuario.id}" not in usuarios:
                await inter.response.send_message("Usuário mencionado não está registrado.")
                return
            
            uid = usuarios[f"{usuario.id}"]
    
    if f"{idAutor}" in usuarios:
        personagensUsuario = gs.get_user_stats(uid)["characters"]
        imagem = Construir_imagem(personagensUsuario)
        await inter.response.send_message(personagensUsuario[0])


@bot.slash_command(name="registrar", description="Registre seu uid ")
async def registrar(inter, uid : int):
    idAutor = inter.author.id
    usuarios[f"{idAutor}"] = uid
    salvar(usuarios, "usuarios")
    await inter.response.send_message("Registrado com sucesso!")



chaves = carregar("keys")
ltuid = chaves["genshinstats"]["ltuid"]
ltoken = chaves["genshinstats"]["ltoken"]
gs.set_cookie(ltuid = ltuid, ltoken = ltoken)

tokenBot = chaves["discord"]
usuarios = carregar("usuarios")
bot.run(tokenBot)
