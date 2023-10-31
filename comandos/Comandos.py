import disnake
from disnake.ext import commands
from outros.GenshinServico import GenshinServico
from outros.ImagemPersonagens import ImagemPersonagens

from outros.save_load import *


class Comandos(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.slash_command(name="github", description="Link para o repositório do Github")
    async def github(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.send_message("[Clique aqui](https://github.com/luizfernandozimmermann/genshinBot) para acessar o repositório.")

    @commands.slash_command(name="personagens", description="Veja seus personagens ou da pessoa mencionada.")
    async def personagens(self, inter : disnake.ApplicationCommandInteraction, usuario : disnake.User = None):
        id_autor = inter.author.id
        await inter.response.defer()
        
        usuarios = carregar()
        id_usuario_selecionado = 0
        if usuario == None:
            if f"{id_autor}" not in usuarios:
                await inter.edit_original_message("Se registre antes de utilizar este comando.")
                return
            
            uid = usuarios[f"{id_autor}"]["uid"]
            id_usuario_selecionado = f"{id_autor}"

        else:
            if f"{usuario.id}" not in usuarios:
                await inter.edit_original_message("Usuário mencionado não está registrado.")
                return
            
            uid = usuarios[f"{usuario.id}"]["uid"]
            id_usuario_selecionado = f"{usuario.id}"
        
        cookies = usuarios[id_usuario_selecionado]
        texto = "Coletando personagens... "
        await inter.edit_original_message(texto)

        try:
            usuario_genshin = await GenshinServico.get_genshin_user(cookies, uid)
        except:
            await inter.edit_original_message(
                "Ocorreu um erro com seu registro, favor utilizar os comandos /remover_registro e /registrar para se registrar novamente.")
            return
        
        texto += "\U00002705\nMontando imagem..."
        await inter.edit_original_message(texto)
        imagem = ImagemPersonagens(usuario_genshin, uid)
        
        await inter.edit_original_message(content="", file=imagem.arquivo_imagem)

    @commands.slash_command(name="ping", description="Ver a latência do bot.")
    async def ping(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Pong! {round(self.bot.latency, 2)}ms", ephemeral=True)


def setup(bot : commands.Bot):
    bot.add_cog(Comandos(bot))
