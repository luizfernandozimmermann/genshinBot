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
        
        usuarios = carregar("usuarios")
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
        
        ltuid = usuarios[id_usuario_selecionado]["ltuid"]
        ltoken = usuarios[id_usuario_selecionado]["ltoken"]

        if f"{id_autor}" in usuarios:
            try:
                usuario_genshin = await GenshinServico.get_full_user_info(ltuid, ltoken, uid)
            except:
                await inter.edit_original_message(
                    "Ocorreu um erro com seu registro, favor utilizar os comandos </remover_registro:1149018837715517460> e </registrar:1138531874877227138> para se registrar novamente.")
                return
            
            usuario_genshin.characters.sort(key=lambda x: (-x.rarity, x.name))
            
            imagem = ImagemPersonagens(usuario_genshin, uid)
            
            await inter.edit_original_message(file=imagem.arquivo_imagem)

    @commands.slash_command(name="registrar", description="Registre sua conta do Genshin.")
    async def registrar(self, inter : disnake.ApplicationCommandInteraction, uid : int, ltuid: int, ltoken: str):
        await inter.response.defer(ephemeral=True)
        usuarios = carregar("usuarios")

        id_autor = inter.author.id
        if str(id_autor) in usuarios:
            await inter.edit_original_message("Você já está registrado.")
            return
        
        try:
            await GenshinServico.get_full_user_info(ltuid, ltoken, uid)
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

    @commands.slash_command(name="remover_registro", description="Remove o registro da sua conta de Genshin.")
    async def remover_registro(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        
        usuarios = carregar("usuarios")
        
        if str(inter.user.id) not in usuarios:
            await inter.edit_original_message("Você não está registrado.")
            return
        
        del usuarios[str(inter.user.id)]
        
        salvar(usuarios, "usuarios")
        
        await inter.edit_original_message("Registro removido com sucesso.")

    @commands.slash_command(name="ping", description="Ver a latência do bot.")
    async def ping(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Pong! {round(self.bot.latency, 2)}ms", ephemeral=True)


def setup(bot : commands.Bot):
    bot.add_cog(Comandos(bot))
