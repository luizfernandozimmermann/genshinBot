import disnake
from disnake.ext import commands


class Ajuda(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @commands.slash_command(name="help", description="Mostra todos os comandos")
    async def help(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        embed = disnake.Embed(
            title="Lista de todos os comandos"
        )
        embed.set_footer(
            text="Caso o Bot esteja com algum problema ou bug, utilize /github e abra uma Issue no repositório."
        )
        
        id_comandos = {
            "ajuda_registro": 1146523873018392596,
            "github": 1148001927351775256,
            "help": 1148001927351775255,
            "personagens": 1138526797873549342,
            "ping": 1147977102017179709,
            "registrar": 1138531874877227138
        }
        
        for nome_comando, id_comando in id_comandos.items():
            comando = self.client.get_slash_command(nome_comando)
            embed.add_field(
                name=f"</{nome_comando}:{id_comando}>",
                value=comando.description,
                inline=False
            )
        
        await inter.edit_original_message(embed=embed)
        
    @commands.slash_command(name="ajuda_registro", description="Tutorial de como registrar sua conta do Genshin.")
    async def ajuda_registro(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        view = self.ViewAjudaRegistro()
        await inter.edit_original_message(view=view, embed=view.embed)


    class ViewAjudaRegistro(disnake.ui.View):
        def __init__(self):
            super().__init__()
            self.pagina = 1
            self.conteudo_paginas = [
                "Entre no site da [Hoyolab](https://www.hoyolab.com/home)",
                "Clique com o botão direito em qualquer área do site e clique em inspecionar (Ou utilize apenas  Control + Shift + C)",
                "Clique nos três pontinhos no canto superior direito",
                "Selecione a terceira imagem onde está escrito 'Dock side'",
                "Vá para a aba 'Application' e procure por 'Cookies' e expanda-o",
                "Clique na única opção que aparece (http://www.hoyolab.com)",
                "Procure por 'ltuid' e copie onde está o 'value'",
                "Depois procure por 'ltoken' e faça a mesma coisa",
                "Agora só é preciso pegar seu UID dentro do jogo e pronto! Você possui tudo para poder se registrar"
            ]
            self.imagem_paginas = [
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974482036801617/ajuda_registro_1.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974482326196314/ajuda_registro_2.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974482632388730/ajuda_registro_3.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974483001491467/ajuda_registro_4.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974483420909679/ajuda_registro_5.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974483664187493/ajuda_registro_6.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974484012318760/ajuda_registro_7.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974481298591744/ajuda_registro_8.png",
                "https://cdn.discordapp.com/attachments/1056255419162574998/1147974481722224750/ajuda_registro_9.png"
            ]
            self.atualizar_embed()
            
        def atualizar_embed(self):
            self.embed = disnake.Embed(
                title = f"Como registrar - Página {self.pagina}\n",
                description =  self.conteudo_paginas[self.pagina - 1]
            )
            self.embed.set_footer(text="ATENÇÃO: Como Cookies de sites contém informações sobre login e senha, este bot não compartilha nenhuma dessas informações. Além disso, NÃO COMPARTILHE COM OUTROS, mas caso aconteça, é recomendável trocar sua senha.")
            
            self.embed.set_image(url=self.imagem_paginas[self.pagina - 1])
        
        async def atualizar_mensagem(self, inter : disnake.ApplicationCommandInteraction):
            await inter.response.edit_message(embed=self.embed, view=self)
            
        @disnake.ui.button(label="<", style=disnake.ButtonStyle.blurple, disabled=True)
        async def botao_anterior(self, button : disnake.ui.Button, inter : disnake.ApplicationCommandInteraction):
            if self.pagina > 1:
                self.pagina -= 1
                
                self.botao_proximo.disabled = False
                self.botao_anterior.disabled = False
                if self.pagina == 1:
                    self.botao_anterior.disabled = True
                    
                self.atualizar_embed()
                await self.atualizar_mensagem(inter)
        
        @disnake.ui.button(label=">", style=disnake.ButtonStyle.blurple)
        async def botao_proximo(self, button : disnake.ui.Button, inter : disnake.ApplicationCommandInteraction):
            if self.pagina < len(self.conteudo_paginas):
                self.pagina += 1
                
                self.botao_anterior.disabled = False
                self.botao_proximo.disabled = False
                if self.pagina == len(self.conteudo_paginas):
                    self.botao_proximo.disabled = True
                    
                self.atualizar_embed()
                await self.atualizar_mensagem(inter)
    

def setup(client: commands.Bot):
    client.add_cog(Ajuda(client))
