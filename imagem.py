from genshin.models.genshin.chronicle.characters import Character
from genshin.models.genshin import FullGenshinUserStats
from disnake import File
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request
import os
from math import ceil

from save_load import carregar


class ImagemPersonagens():
    def __init__(self, usuario : FullGenshinUserStats, uid : int):
        self.USUARIO = usuario
        self.UID = uid
        self.fonte_genshin_12 = ImageFont.truetype("fonte_texto_genshin.ttf", 12)
        self.PERSONAGENS_ALIAS : dict = carregar("char_alias")
        self.construir_imagem_personagens()
    
    def construir_imagem_personagens(self) -> File:
        self.largura_imagem = 1390
        self.altura_imagem = 328 + ceil(len(self.USUARIO.characters) / 11) * 140
        
        self.criar_base()
        self.adicionar_info_superior()
        self.adicionar_personagens()
        self.adicionar_estatistica_personagens()
        self.adicionar_info_inferior()

        image_buffer = io.BytesIO()
        self.imagem.save(image_buffer, format='PNG')
        image_buffer.seek(0)

        self.arquivo_imagem = File(image_buffer, filename='image.png')
        image_buffer.close()

    def criar_base(self):
        self.imagem = Image.new(mode="RGBA", 
                                size=(self.largura_imagem, self.altura_imagem),
                                color="#3d4754")
        
        # linha maior
        self.draw = ImageDraw.Draw(self.imagem)
        self.fonte_genshin_12.getmask("").getbbox
        self.draw.rounded_rectangle([(5, 5), (self.largura_imagem - 5, self.altura_imagem - 5)],
                    outline = "#ffd4c1", fill = None, radius = 50, width=5)
        
        # linha menor
        self.draw.rounded_rectangle([(19, 19), (self.largura_imagem - 19, self.altura_imagem - 19)],
                    outline = "#9e8e8b", fill = None, radius = 40, width=4)

    def adicionar_info_superior(self):
        self.draw.line([(43, 46), (43, 77)], width=2, fill="#9e8e8b")
        fonte_genshin_12 = ImageFont.truetype("fonte_texto_genshin.ttf", 16)

        self.draw.text(
            (50, 45), 
            f"Usuário: {self.USUARIO.info.nickname}\nRank de Aventura: {self.USUARIO.info.level}",
            font = fonte_genshin_12,
            fill="#ffd4c1",
            spacing=-1
        )

        self.draw.rounded_rectangle(
            (550, 45, 550 + 310, 45 + 35),
            radius=50,
            fill="#1f242b"
        )
        
        self.draw.line([(1345, 46), (1345, 77)], width=2, fill="#9e8e8b")

        self.draw.text(
            (1194, 45),
            f"Servidor: {self.pegar_servidor()}\nUID: {self.UID}",
            font = fonte_genshin_12,
            fill="#ffd4c1",
            spacing=-1,
            align="right"
        )

    def adicionar_personagens(self):
        posicao_y = 0
        for pos, personagem in enumerate(self.USUARIO.characters):
            personagem = self.Personagem(personagem, self.PERSONAGENS_ALIAS, self.fonte_genshin_12)
                
            if pos % 11 == 0 and pos != 0:
                posicao_y += 1
                
            self.imagem.paste(personagem.imagem, 
                            ((110 + 10) * (pos % 11) + 40, posicao_y * (133 + 7) + 100),
                                mask=personagem.imagem)

    def adicionar_estatistica_personagens(self):
        quantidades = {
            "pyro":     sum(personagem.element == "Pyro"    for personagem in self.USUARIO.characters),
            "anemo":    sum(personagem.element == "Anemo"   for personagem in self.USUARIO.characters),
            "geo":      sum(personagem.element == "Geo"     for personagem in self.USUARIO.characters),
            "hydro":    sum(personagem.element == "Hydro"   for personagem in self.USUARIO.characters),
            "cryo":     sum(personagem.element == "Cryo"    for personagem in self.USUARIO.characters),
            "electro":  sum(personagem.element == "Electro" for personagem in self.USUARIO.characters),
            "dendro":   sum(personagem.element == "Dendro"  for personagem in self.USUARIO.characters),
            "5-Estrelas": sum(personagem.rarity == 5 for personagem in self.USUARIO.characters),
            "4-Estrelas": sum(personagem.rarity == 4 for personagem in self.USUARIO.characters)
        }
        
        fonte_genshin_16 = ImageFont.truetype("fonte_texto_genshin.ttf", 16)
        pos_x = 40
        pos_y = self.altura_imagem - 215
        for chave, valor in quantidades.items():
            if chave in ["5-Estrelas", "4-Estrelas"]:
                simbolo = Image.open("imagens_base/estatistica_" + chave + ".png").convert("RGBA")
            else:
                simbolo = Image.open("imagens_base/elemento_" + chave + ".png").convert("RGBA").resize((24, 24))

            texto = f"{chave.capitalize()}     {valor}"
            largura_texto = fonte_genshin_16.getmask(texto).getbbox()[2]
            tamanho = 40 + largura_texto + 12
            
            if pos_x + 39 + largura_texto + 14 >= 1350:
                pos_x = 40
                pos_y += 35

            self.draw.rounded_rectangle(
                ((pos_x, pos_y), (pos_x + tamanho, pos_y + 30)),
                radius=50,
                fill="#21272e"
            )

            self.imagem.paste(
                simbolo,
                (pos_x + 5, pos_y + 4),
                mask = simbolo
            )

            self.draw.text(
                (pos_x + 39, pos_y + 5),
                texto,
                fill="#ffffff",
                font=fonte_genshin_16
            )

            pos_x += tamanho + 6

    def adicionar_info_inferior(self):
        self.draw.text(
            (35, self.altura_imagem - 94),
    """*Informações podem devido às limitações da API da HoYoLAB
    Veja dentro do jogo para informações mais precisas
    """,
            font=self.fonte_genshin_12,
            fill="#ffd4c1"
        )

        texto = """Este bot foi inteiramente inspirado em Genshin Wizard
    Acesse o discord oficial deles: discord.gg/genshinwizard
    """
        largura_texto = self.fonte_genshin_12.getmask(texto).getbbox()[2]
        self.draw.text(
            (1355 - largura_texto, self.altura_imagem - 94),
            texto,
            font=self.fonte_genshin_12,
            fill="#ffd4c1",
            align="right"
        )
        
        fonte_genshin_24 = ImageFont.truetype("fonte_texto_genshin.ttf", 24)
        self.draw.text(
            (562, 48),
            "Resumo do Personagem",
            fill="#ffd4c1",
            font=fonte_genshin_24
        )

        self.draw.line(
            [(45, self.altura_imagem - 122), (1344, self.altura_imagem - 122)],
            fill="#50555f",
            width=2
        )
        
    def pegar_servidor(self):
        num_server = str(self.UID)[0]
        if num_server in ["1", "2", "5"]:
            return "Mainland China"

        if num_server == "6":
            return "America"
        
        if num_server == "7":
            return "Europa"
        
        if num_server == "8":
            return "Asia"
        
        if num_server == "9":
            return "Taiwan, Hong Kong, Macao"

    class Personagem():
        def __init__(self, personagem : Character, personagens_alias, fonte_genshin12 : ImageFont):
            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
                ]
            urllib.request.install_opener(opener)
            
            self.info = personagem
            self.FONTE_GENSHIN_12 = fonte_genshin12
            self.PERSONAGENS_ALIAS = personagens_alias
            self.caminho_imagem = "imagens/personagens/icone_" + self.info.name.lower().replace(" ", "_") + ".png"
            self.construir_icone()
            self.draw = ImageDraw.Draw(self.imagem)
            self.preencher_info()
        
        def construir_icone(self):
            if self.info.name == "Traveler":
                self.caminho_imagem = "imagens/personagens/icone_aether.png"
                if "Girl" in self.info.icon:
                    self.caminho_imagem = "imagens/personagens/icone_lumine.png"
                    
            if not os.path.isfile(self.caminho_imagem):
                self.criar_imagem_nova()
                self.imagem = Image.open(self.caminho_imagem).convert("RGBA")

            self.imagem = Image.open(self.caminho_imagem).convert("RGBA")

        def criar_imagem_nova(self):
            # MALDITA API QUE ESCREVEU O NOME DOS PERSONAGENS ERRADO AAAAAAAAAAAAAAAAAAAAAAAAA
            print(self.info.name)
            nome_personagem = self.info.name
            if self.info.name == "Traveler":
                nome_personagem = "PlayerBoy"
                if "Girl" in self.info.icon:
                    nome_personagem = "PlayerGirl"
            
            try:
                urllib.request.urlretrieve(self.info.icon, self.caminho_imagem)
                    
                imagem_personagem_novo = Image.open(self.caminho_imagem).resize((110, 110))
            except:
                if self.info.name in self.PERSONAGENS_ALIAS:
                    for alias in self.PERSONAGENS_ALIAS[self.info.name]:
                        try:
                            urllib.request.urlretrieve(f"https://api.ambr.top/assets/UI/UI_AvatarIcon_{alias}.png", self.caminho_imagem) 
                    
                            imagem_personagem_novo = Image.open(self.caminho_imagem).resize((110, 110))
                        except:
                            pass
                else:
                    urllib.request.urlretrieve(f"https://api.ambr.top/assets/UI/UI_AvatarIcon_{nome_personagem}.png", self.caminho_imagem) 
                    
                    imagem_personagem_novo = Image.open(self.caminho_imagem).resize((110, 110))

            self.PersonagemNovoConstrutor(imagem_personagem_novo, self.info) \
                .construir_e_salvar_personagem_imagem()

        def preencher_info(self):
            if self.info.name == "Traveler":
                self.adicionar_elemento()

            # Nível
            self.draw.text((6, 90), "Lv. " + str(self.info.level), font = self.FONTE_GENSHIN_12)

            # Amizade
            self.draw.text((89, 90), str(self.info.friendship), font = self.FONTE_GENSHIN_12)

            # Constelação
            self.draw.text((87, 5), "C" + str(self.info.constellation), font = self.FONTE_GENSHIN_12)

        def adicionar_elemento(self):
            caminho_imagem_elemento = "imagens_base/elemento_" + self.info.element.lower() + ".png"
            imagem_elemento = Image.open(caminho_imagem_elemento).resize((26, 26)).convert("RGBA")
            self.imagem.paste(imagem_elemento, mask= imagem_elemento, box = (4, 4))

    
        class PersonagemNovoConstrutor():
            def __init__(self, imagem_personagem : Image, personagem : Character):
                self.fill = (0, 0, 0, 230)
                self.imagem = imagem_personagem
                self.personagem = personagem

            def construir_e_salvar_personagem_imagem(self) -> Image:
                self.adicionar_raridade_fundo()
                self.adicionar_nome_personagem()
                self.adicionar_fundo_infos()
                self.adicionar_elemento_fundo()

                caminho_imagem = "imagens/personagens/icone_" + self.personagem.name.lower().replace(" ", "_") + ".png"
                if self.personagem.name == "Traveler":
                    caminho_imagem = "imagens/personagens/icone_aether.png"
                    if "Girl" in self.personagem.icon:
                        caminho_imagem = "imagens/personagens/icone_lumine.png"
                        
                self.imagem.save(caminho_imagem)
                
            def adicionar_raridade_fundo(self):
                raridade = self.personagem.rarity
                if self.personagem.name == "Aloy":
                    raridade = 3

                caminho_imagem_fundo = "imagens_base/fundo_" + str(raridade) + "_estrelas.png"

                imagem = Image.open(caminho_imagem_fundo)
                imagem.paste(self.imagem, mask=self.imagem)
                self.imagem = imagem
                
            def adicionar_nome_personagem(self):
                font = ImageFont.truetype("fonte_texto_genshin.ttf", 16)
                draw = ImageDraw.Draw(self.imagem)
                largura_texto = font.getmask(self.personagem.name).getbbox()[2]
                altura_texto = font.getmask(self.personagem.name).getbbox()[3] + font.getmetrics()[1]

                nome_alterado = self.personagem.name
                letras_a_menos = 0
                while largura_texto >= 110:
                    letras_a_menos += 1
                    nome_alterado = self.personagem.name[:-letras_a_menos] + "..."
                    largura_texto = font.getmask(nome_alterado).getbbox()[2]
                    altura_texto = font.getmask(self.personagem.name).getbbox()[3] + font.getmetrics()[1]

                draw.text(
                    ((110 - largura_texto) / 2, 110 + (21 - altura_texto) / 2), 
                    text=nome_alterado, 
                    fill=(40, 40, 40), 
                    font=font)
                
            def adicionar_fundo_infos(self):
                fundo = Image.open("imagens_base/fundo_infos_personagens.png").convert("RGBA")
                
                self.imagem.paste(fundo, (0, 0), mask=fundo)

            def adicionar_elemento_fundo(self):
                if self.personagem.name != "Traveler":
                    caminho_imagem_elemento = "imagens_base/elemento_" + self.personagem.element.lower() + ".png"
                    imagem_elemento = Image.open(caminho_imagem_elemento).resize((26, 26)).convert("RGBA")
                    self.imagem.paste(imagem_elemento, mask= imagem_elemento, box = (4, 4))
