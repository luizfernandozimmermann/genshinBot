import disnake
from disnake.ext import commands

import funcoes_genshin as fg
import asyncio

from save_load import *
from imagem import *


bot = commands.Bot(command_prefix="*")

@bot.slash_command(name="personagens", description="Veja seus personagens ou da pessoa mencionada.")
async def personagens(inter, usuario : disnake.User = None):
    id_autor = inter.author.id
    await inter.response.defer()

    id_usuario_selecionado = 0
    if usuario == None:
        if f"{id_autor}" not in usuarios:
            await inter.edit_original_message("Registre seu uid.")
            return
        
        uid = usuarios[f"{id_autor}"]["uid"]
        id_usuario_selecionado = f"{id_autor}"

    else:
        if f"{usuario.id}" not in usuarios:
            await inter.edit_original_message("Usuário mencionado não está registrado.")
            return
        
        uid = usuarios[f"{usuario.id}"]["uid"]
        id_usuario_selecionado = f"{usuario.id}"
    
    ltuid = usuarios[id_usuario_selecionado]["ltuid"]
    ltoken = usuarios[id_usuario_selecionado]["ltoken"]

    if f"{id_autor}" in usuarios:
        personagens_usuario = await fg.get_characters(ltuid, ltoken, uid)
        personagens_usuario.sort(key=lambda x: (-x.rarity, x.name))
        
        usuario_genshin = await fg.get_user_info(ltuid, ltoken, uid)
        imagem = Construir_imagem_personagens(personagens_usuario, 
                                              usuario_genshin.info.nickname,
                                              uid,
                                              usuario_genshin.info.level)
        await inter.edit_original_message(file=imagem)


@bot.slash_command(name="registrar", description="Registre seu uid ")
async def registrar(inter, uid : int, ltuid: int, ltoken: str):
    await inter.response.defer()

    id_autor = inter.author.id
    if str(id_autor) in usuarios:
        await inter.edit_original_message("Você já está registrado.")
        return
    
    try:
        resposta = asyncio.run(fg.get_characters(ltuid, ltoken, uid))
    except:
        await inter.edit_original_message("Algo deu errado. Verifique o uid, ltuid e o ltoken.")
        return
    
    usuarios[f"{id_autor}"] = {
        "uid": uid,
        "ltuid": ltuid,
        "ltoken": ltoken
    }
    salvar(usuarios, "usuarios")
    await inter.edit_original_message("Registrado com sucesso!")


@bot.slash_command(name="ajuda_registro", description="Tutorial de como registrar sua conta do genshin.")
async def ajuda_registro(inter):
    embed = disnake.Embed(title="Como registrar", 
                          description="1. Entre  no site da [Hoyolab](https://www.hoyolab.com/home) \n" +
                                      "2. Certifique que está logado no site"+
                                      "3. Clique com o botão direito em qualquer parte do site e clique em Inspecionar")
    await inter.response.send_message(embed = embed)


chaves = carregar("keys")
tokenBot = chaves["discord"]
usuarios = carregar("usuarios")
bot.run(tokenBot)
