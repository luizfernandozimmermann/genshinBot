import disnake
from disnake.ext import commands
from outros.GenshinServico import GenshinServico

from outros.save_load import *


def registrar(cookies : dict, id_usuario : str):
    usuarios = carregar()
    usuarios[id_usuario] = cookies
    salvar(usuarios)
    
    
class Registro(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
    @commands.slash_command(name="registrar", description="Registre sua conta do Genshin.")
    async def registrar(self, inter_comando : disnake.ApplicationCommandInteraction):
        await inter_comando.response.defer(ephemeral=True)
        
        if str(inter_comando.user.id) in carregar():
            await inter_comando.edit_original_message("Você já está registrado.")
            return
                
        embed_escolha = disnake.Embed(
            title=f"Registro em {self.bot.user.display_name}",
            description="Clique no botão para selecionar o método que gostaria de usar.",
            colour=disnake.Colour.blue()
        )

        class RegistroEscolhaView(disnake.ui.View):
            @disnake.ui.button(label="Manual", emoji="\U0001F590", style=disnake.ButtonStyle.blurple)
            async def botao_escolha_manual(self, button: disnake.ui.Button, botao_escolha_inter: disnake.MessageInteraction):
                await botao_escolha_inter.response.defer()

                class RegistroManualView(disnake.ui.View):
                    class RegistroManualModal(disnake.ui.Modal):
                        def __init__(self):
                            super().__init__(
                                title="Registro manual", 
                                components=[
                                    disnake.ui.TextInput(label="UID da sua conta", style=disnake.TextInputStyle.short, placeholder="uid", custom_id="uid", min_length=9, max_length=9),
                                    disnake.ui.TextInput(label="ltmid_v2 da HoyoLab", style=disnake.TextInputStyle.short, placeholder="ltmid", custom_id="ltmid_v2"),
                                    disnake.ui.TextInput(label="ltoken_v2 da HoyoLab", style=disnake.TextInputStyle.short, placeholder="ltoken", custom_id="ltoken_v2")
                                    ]
                                )
                        
                        async def callback(self, inter : disnake.ModalInteraction):
                            await inter.response.defer(ephemeral=True)
                            
                            cookies = inter.text_values
                            uid = int(cookies["uid"])
                            cookies["uid"] = uid
                            valido = await GenshinServico.checar_usuario_valido(cookies, uid)
                            
                            if valido:
                                registrar(cookies, str(inter.user.id))
                                await inter_comando.edit_original_message("Registrado!", embed=None, view=None)
                                await inter.edit_original_message("Registrado com sucesso!")
                            else:
                                await inter.edit_original_message("Registro falhou. Verifique se as informações estão corretas. Caso o erro persista, contate o dono do bot.")
                            
                            
                    @disnake.ui.button(label="Voltar", style=disnake.ButtonStyle.red)
                    async def botao_registro_manual_voltar(self, button: disnake.ui.Button, botao_inter: disnake.MessageInteraction):
                        await botao_inter.response.defer()
                        view_escolha = RegistroEscolhaView()
                        await inter_comando.edit_original_message(embed=embed_escolha, view=view_escolha)
                        
                    @disnake.ui.button(label="Registrar", style=disnake.ButtonStyle.green)
                    async def botao_registro_manual_registrar(self, button: disnake.ui.Button, botao_inter: disnake.MessageInteraction):
                        modal = self.RegistroManualModal()
                        await botao_inter.response.send_modal(modal)
                
                view_registro = RegistroManualView()
                embed_registro = disnake.Embed(
                    title="Registro Manual",
                    description="Para se registrar pelo método manual, você terá que usar o comando /ajuda_registro e seguir os passos.",
                    colour=disnake.Colour.blue()
                )

                await inter_comando.edit_original_message(embed=embed_registro, view=view_registro)
                
            # @disnake.ui.button(label="Script", emoji="\U0000270D", style=disnake.ButtonStyle.blurple)
            # async def botao_escolha_script(self, button: disnake.ui.Button, botao_escolha_inter: disnake.MessageInteraction):
            #     await botao_escolha_inter.response.defer()
                
            #     class RegistroScriptView(disnake.ui.View):
            #         class RegistroScriptModal(disnake.ui.Modal):
            #             def __init__(self):
            #                 super().__init__(
            #                     title="Registro por script", 
            #                     components=[
            #                         disnake.ui.TextInput(label="UID da sua conta", style=disnake.TextInputStyle.short, placeholder="uid", custom_id="uid", min_length=9, max_length=9),
            #                         disnake.ui.TextInput(label="Cookies copiados", style=disnake.TextInputStyle.short, placeholder="Cookies", custom_id="cookies")
            #                         ]
            #                     )

            #             async def callback(self, inter : disnake.ModalInteraction):
            #                 await inter.response.defer(ephemeral=True)

            #                 cookies : dict = eval(inter.text_values["cookies"])
            #                 uid = int(inter.text_values["uid"])
            #                 cookies["uid"] = uid
            #                 valido = await GenshinServico.checar_usuario_valido(cookies, uid)
                            
            #                 if valido:
            #                     registrar(cookies, str(inter.user.id))
            #                     await inter.edit_original_message("Registrado com sucesso!")
            #                     await inter_comando.edit_original_message("Registrado!", embed=None, view=None)
            #                 else:
            #                     await inter.edit_original_message("Registro falhou. Verifique se as informações estão corretas. Caso o erro persista, contate o dono do bot.")

            #         @disnake.ui.button(label="Voltar", style=disnake.ButtonStyle.red)
            #         async def botao_registro_script_voltar(self, button: disnake.ui.Button, botao_inter: disnake.MessageInteraction):
            #             await botao_inter.response.defer()
            #             view_escolha = RegistroEscolhaView()
            #             await inter_comando.edit_original_message(embed=embed_escolha, view=view_escolha)
                        
            #         @disnake.ui.button(label="Registrar", style=disnake.ButtonStyle.green)
            #         async def botao_registro_script_registrar(self, button: disnake.ui.Button, botao_inter: disnake.MessageInteraction):
            #             modal = self.RegistroScriptModal()
            #             await inter_comando.edit_original_message(embed=embed_escolha, view=view_escolha)
            #             await botao_inter.response.send_modal(modal)
                
            #     view_registro = RegistroScriptView()
            #     embed_registro = disnake.Embed(
            #         title="Registro por Script",
            #         description="Para se registrar pelo método script, você terá que copiar o script abaixo, então acessar o site da [Hoyolab](https://www.hoyolab.com) e assim que a página carregar, escreva 'java' na barra de URL do navegador e então cole o script . Depois que aparecer a mensagem de sucesso, volte e cole os cookies que foram copiados.",
            #         colour=disnake.Colour.blue()
            #     )
            #     embed_registro.add_field(name="Script", value=r"```script:var inputElement = document.createElement('input'); var cookies = document.cookie.split('; ').reduce((prev, current) => { const [name, ...value] = current.split('='); prev[name] = value.join('='); return prev; }, {}); inputElement.value = `{'ltoken_v2':'${cookies.ltoken_v2}', 'ltmid_v2':'${cookies.ltmid_v2}'}`; document.body.appendChild(inputElement); inputElement.select(); document.execCommand('copy'); document.body.removeChild(inputElement); alert('Copiado com sucesso!');```")

            #     await inter_comando.edit_original_message(embed=embed_registro, view=view_registro)

        view_escolha = RegistroEscolhaView()
        
        await inter_comando.edit_original_message(embed=embed_escolha, view=view_escolha)

    @commands.slash_command(name="remover_registro", description="Remove o registro da sua conta de Genshin.")
    async def remover_registro(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        
        usuarios = carregar()
        
        if str(inter.user.id) not in usuarios:
            await inter.edit_original_message("Você não está registrado.")
            return
        
        del usuarios[str(inter.user.id)]
        
        salvar(usuarios, "usuarios")
        
        await inter.edit_original_message("Registro removido com sucesso.")


def setup(bot : commands.Bot):
    bot.add_cog(Registro(bot))
