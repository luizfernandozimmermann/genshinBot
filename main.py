import disnake
from disnake.ext import commands

import funcoes_genshin as fg
import asyncio

from save_load import *
from imagem import *


bot = commands.Bot(command_prefix="!")
bot.load_extension("ajuda")

@bot.slash_command(name="personagens", description="Veja seus personagens ou da pessoa mencionada.")
async def personagens(inter : disnake.ApplicationCommandInteraction, usuario : disnake.User = None):
    id_autor = inter.author.id
    await inter.response.defer()
    
    usuarios = carregar("usuarios")
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
        usuario_genshin = await fg.get_full_user_info(ltuid, ltoken, uid)
        usuario_genshin.characters.sort(key=lambda x: (-x.rarity, x.name))
        
        imagem = ImagemPersonagens(usuario_genshin, uid)
        
        await inter.edit_original_message(file=imagem.arquivo_imagem)

@bot.slash_command(name="registrar", description="Registre sua conta do Genshin.")
async def registrar(inter : disnake.ApplicationCommandInteraction, uid : int, ltuid: int, ltoken: str):
    await inter.response.defer(ephemeral=True)
    usuarios = carregar("usuarios")

    id_autor = inter.author.id
    if str(id_autor) in usuarios:
        await inter.edit_original_message("Você já está registrado.")
        return
    
    try:
        await fg.get_full_user_info(ltuid, ltoken, uid)
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

@bot.slash_command(name="ping", description="Ver a latência do bot.")
async def pint(inter : disnake.ApplicationCommandInteraction):
    await inter.response.send_message(f"Pong! {round(bot.latency, 2)}ms", ephemeral=True)

chaves = carregar("keys")
tokenBot = chaves["discord"]
bot.run(tokenBot)
