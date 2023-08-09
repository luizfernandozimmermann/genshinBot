import disnake
from disnake.ext import commands

import genshinstats as gs

from save_load import *
from imagem import *


bot = commands.Bot(command_prefix="*")

@bot.slash_command(name="personagens", description="Veja seus personagens ou da pessoa mencionada.")
async def personagens(inter, usuario : disnake.User = None):
    id_autor = inter.author.id

    id_usuario_selecionado = 0
    if usuario == None:
        if f"{id_autor}" not in usuarios:
            await inter.response.send_message("Registre seu uid.")
            return
        
        uid = usuarios[f"{id_autor}"]["uid"]
        id_usuario_selecionado = f"{id_autor}"

    else:
        if f"{usuario.id}" not in usuarios:
            await inter.response.send_message("Usuário mencionado não está registrado.")
            return
        
        uid = usuarios[f"{usuario.id}"]["uid"]
        id_usuario_selecionado = f"{usuario.id}"
    
    ltuid = usuarios[id_usuario_selecionado]["ltuid"]
    ltoken = usuarios[id_usuario_selecionado]["ltoken"]
    gs.set_cookie(ltuid = ltuid, ltoken = ltoken)
    
    if f"{id_autor}" in usuarios:
        personagens_usuario = gs.get_user_stats(uid)["characters"]
        imagem = Construir_imagem_personagens(personagens_usuario)
        await inter.response.send_message(file=imagem)


@bot.slash_command(name="registrar", description="Registre seu uid ")
async def registrar(inter, uid : int, ltuid: int, ltoken: str):
    id_autor = inter.author.id
    if str(id_autor) in usuarios:
        await inter.response.send_message("Você já está registrado.")
        return
    
    gs.set_cookie(ltuid = ltuid, ltoken = ltoken)

    try:
        resposta = gs.get_user_stats(uid)["characters"]
    except:
        await inter.response.send_message("Algo deu errado. Verifique o uid, ltuid e o ltoken.")
        return
    
    usuarios[f"{id_autor}"] = {
        "uid": uid,
        "ltuid": ltuid,
        "ltoken": ltoken
    }
    salvar(usuarios, "usuarios")
    await inter.response.send_message("Registrado com sucesso!")


chaves = carregar("keys")
tokenBot = chaves["discord"]
usuarios = carregar("usuarios")
bot.run(tokenBot)
