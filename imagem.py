from genshin.models.genshin.chronicle.characters import Character
from disnake import File
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request
import os
from math import ceil
from typing import List

def Construir_imagem_personagens(personagens, usuario, uid, ar_conta):
    servidor = Pegar_servidor(uid)

    largura_imagem = 1390
    altura_imagem = 328 + ceil(len(personagens) / 11) * 140
    imagem_fundo = Image.new(mode="RGBA", 
                             size=(largura_imagem, altura_imagem),
                             color="#3d4754")
    
    # linha maior
    draw = ImageDraw.Draw(imagem_fundo)
    draw.rounded_rectangle([(5, 5), (largura_imagem - 5, altura_imagem - 5)],
                   outline = "#ffd4c1", fill = None, radius = 50, width=5)
    
    # linha menor
    draw.rounded_rectangle([(19, 19), (largura_imagem - 19, altura_imagem - 19)],
                   outline = "#9e8e8b", fill = None, radius = 40, width=4)

    posicao_y = 0
    fonte_modificacao_personagem = ImageFont.truetype("fonte_texto_genshin.ttf", 12)
    for pos, personagem in enumerate(personagens):
        imagem_personagem = Construir_icone_personagem(personagem, fonte_modificacao_personagem)

        if pos % 11 == 0 and pos != 0:
            posicao_y += 1

        imagem_fundo.paste(imagem_personagem, 
                           ((110 + 10) * (pos % 11) + 40, 
                            posicao_y * (133 + 7) + 100),
                            mask=imagem_personagem)

    draw.line([(43, 46), (43, 77)], width=2, fill="#9e8e8b")
    fonte_modificacao_personagem = ImageFont.truetype("fonte_texto_genshin.ttf", 16)

    draw.text(
        (50, 45), 
        f"Usuário: {usuario}\nRank de Aventura: {ar_conta}",
        font = fonte_modificacao_personagem,
        fill="#ffd4c1",
        spacing=-1
    )

    draw.rounded_rectangle(
        (550, 45, 550 + 310, 45 + 35),
        radius=50,
        fill="#1f242b"
    )
    
    draw.line([(1345, 46), (1345, 77)], width=2, fill="#9e8e8b")

    draw.text(
        (1194, 45),
        f"Servidor: {servidor}\nUID: {uid}",
        font = fonte_modificacao_personagem,
        fill="#ffd4c1",
        spacing=-1,
        align="right"
    )
    
    imagem_fundo = Adicionar_estatistica_personagens(imagem_fundo, personagens, fonte_modificacao_personagem, altura_imagem)

    draw.text(
        (35, altura_imagem - 94),
"""*Informações podem devido às limitações da API da HoYoLAB
Veja dentro do jogo para informações mais precisas
""",
        font=fonte_modificacao_personagem,
        fill="#ffd4c1"
    )

    texto = """Este bot foi inteiramente inspirado em Genshin Wizard
Acesse o discord oficial deles: discord.gg/genshinwizard
"""
    largura_texto, altura_texto = draw.textsize(texto, fonte_modificacao_personagem)
    draw.text(
        (1355 - largura_texto, altura_imagem - 94),
        texto,
        font=fonte_modificacao_personagem,
        fill="#ffd4c1",
        align="right"
    )
    
    fonte_modificacao_personagem = ImageFont.truetype("fonte_texto_genshin.ttf", 24)
    draw.text(
        (562, 48),
        "Resumo do Personagem",
        fill="#ffd4c1",
        font=fonte_modificacao_personagem
    )

    draw.line(
        [(45, altura_imagem - 122), (1344, altura_imagem - 122)],
        fill="#50555f",
        width=2
    )

    image_buffer = io.BytesIO()
    imagem_fundo.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    arquivo = File(image_buffer, filename='image.png')
    image_buffer.close()
    return arquivo


def Adicionar_estatistica_personagens(imagem : Image, personagens : List[Character], font : ImageFont, altura_imagem : int) -> Image:
    quantidades = {
        "pyro": sum(personagem.element == "Pyro" for personagem in personagens),
        "anemo": sum(personagem.element == "Anemo" for personagem in personagens),
        "geo": sum(personagem.element == "Geo" for personagem in personagens),
        "hydro": sum(personagem.element == "Hydro" for personagem in personagens),
        "cryo": sum(personagem.element == "Cryo" for personagem in personagens),
        "electro": sum(personagem.element == "Electro" for personagem in personagens),
        "dendro": sum(personagem.element == "Dendro" for personagem in personagens),
        "5-Estrelas": sum(personagem.rarity == 5 for personagem in personagens),
        "4-Estrelas": sum(personagem.rarity == 4 for personagem in personagens)
    }
    
    pos_x = 40
    pos_y = altura_imagem - 215
    draw = ImageDraw.Draw(imagem)
    for chave, valor in quantidades.items():
        if chave in ["5-Estrelas", "4-Estrelas"]:
            simbolo = Image.open("imagens_base/estatistica_" + chave + ".png").convert("RGBA")
        else:
            simbolo = Image.open("imagens_base/elemento_" + chave + ".png").convert("RGBA").resize((24, 24))

        texto = f"{chave.capitalize()}     {valor}"
        largura_texto, altura_texto = draw.textsize(texto, font)
        tamanho = 40 + largura_texto + 12
        
        if pos_x + 39 + largura_texto + 14 >= 1350:
            pos_x = 40
            pos_y += 35

        draw.rounded_rectangle(
            ((pos_x, pos_y), (pos_x + tamanho, pos_y + 30)),
            radius=50,
            fill="#21272e"
        )

        imagem.paste(
            simbolo,
            (pos_x + 5, pos_y + 4),
            mask = simbolo
        )

        draw.text(
            (pos_x + 39, pos_y + 5),
            texto,
            fill="#ffffff",
            font=font
        )

        pos_x += tamanho + 6

    return imagem


def Pegar_servidor(uid : int):
    numero = str(uid)[0]
    if numero in ["1", "2", "5"]:
        return "Mainland China"

    if numero == "6":
        return "America"
    
    if numero == "7":
        return "Europa"
    
    if numero == "8":
        return "Asia"
    
    if numero == "9":
        return "Taiwan, Hong Kong, Macao"


def Construir_icone_personagem(personagem : Character, fonte_modificacao_personagem):
    caminho_imagem = "imagens/icone_" + personagem.name.lower().replace(" ", "_") + ".png"
    
    if not os.path.isfile(caminho_imagem):
        Criar_imagem_personagem_novo(personagem, caminho_imagem)

    imagem_personagem = Image.open(caminho_imagem).convert("RGBA")
    imagem_personagem = Modificar_imagem_personagem(personagem, imagem_personagem, fonte_modificacao_personagem)
    return imagem_personagem


def Modificar_imagem_personagem(personagem : Character, imagem_personagem, fonte_modificacao_personagem):
    draw = ImageDraw.Draw(imagem_personagem)

    if personagem.name == "Traveler":
        imagem_personagem = Adicionar_elemento_personagem(imagem_personagem, personagem.element)

    # Nível
    draw.text((6, 90), "Lv. " + str(personagem.level).zfill(2), font = fonte_modificacao_personagem)

    # Amizade
    draw.text((89, 90), str(personagem.friendship).zfill(2), font = fonte_modificacao_personagem)

    # Constelação
    draw.text((87, 5), "C" + str(personagem.constellation), font = fonte_modificacao_personagem)

    return imagem_personagem


def Criar_imagem_personagem_novo(personagem : Character, caminho_imagem : str):
    if personagem.name != "Kirara":
        if personagem.name == "Traveler":
            caminho_imagem.replace("traveler", "aether")
            if "Girl" in personagem.icon:
                caminho_imagem.replace("traveler", "lumine")
                
        urllib.request.urlretrieve(personagem.icon, caminho_imagem)
        imagem_personagem_novo = Image.open(caminho_imagem).resize((110, 110))

    else:
        imagem_personagem_novo = Image.open("imagens_base/icone_base_kirara.png").resize((110, 110))

    Construtor_personagem_novo(imagem_personagem_novo) \
        .Construir_e_salvar_personagem_imagem(personagem)


def Adicionar_elemento_personagem(imagem_personagem : Image, elemento : str):
    caminho_imagem_elemento = "imagens_base/elemento_" + elemento.lower() + ".png"
    imagem_elemento = Image.open(caminho_imagem_elemento).resize((26, 26)).convert("RGBA")
    imagem_personagem.paste(imagem_elemento, mask= imagem_elemento, box = (4, 4))
    return imagem_personagem


class Construtor_personagem_novo():
    fill = (0, 0, 0, 230)
    radius = 10
    imagem : Image

    def __init__(self, imagem_personagem : Image):
        self.imagem = imagem_personagem

    def Construir_e_salvar_personagem_imagem(self, personagem : Character) -> Image:
        self.Adicionar_raridade_fundo(personagem.rarity, personagem.name)
        self.Adicionar_nome_personagem(personagem.name)
        self.Adicionar_elemento_fundo(personagem.element, personagem.name)
        self.Adicionar_constelacao_fundo()
        self.Adicionar_amizade_fundo()
        self.Adicionar_nivel_fundo()

        self.imagem.save("imagens/icone_" + personagem.name.lower().replace(" ", "_") + ".png")
    
    def Adicionar_elemento_fundo(self, elemento : str, nome_personagem : str):
        draw = ImageDraw.Draw(self.imagem)
        draw.rounded_rectangle(((3, 3), (30, 31)), radius = self.radius, fill = (20, 20, 20, 230))

        if nome_personagem != "Traveler":
            self.imagem = Adicionar_elemento_personagem(self.imagem, elemento)

    def Adicionar_nome_personagem(self, nome_personagem : str):
        font = ImageFont.truetype("fonte_texto_genshin.ttf", 16)
        draw = ImageDraw.Draw(self.imagem)
        largura_texto, altura_texto = draw.textsize(nome_personagem, font)

        nome_alterado = nome_personagem
        letras_a_menos = 0
        while largura_texto >= 110:
            letras_a_menos += 1
            nome_alterado = nome_personagem[:-letras_a_menos] + "..."
            largura_texto, altura_texto = draw.textsize(nome_alterado, font)

        draw.text(
            ((110 - largura_texto) / 2, 110 + (21 - altura_texto) / 2), 
            text=nome_alterado, 
            fill=(40, 40, 40), 
            font=font)

    def Adicionar_raridade_fundo(self, raridade : int, nome_personagem : str):
        if nome_personagem == "Aloy":
            raridade = 3

        caminho_imagem_fundo = "imagens_base/fundo_" + str(raridade) + "_estrelas.png"

        imagem = Image.open(caminho_imagem_fundo)
        imagem.paste(self.imagem, mask=self.imagem)
        self.imagem = imagem

    def Adicionar_constelacao_fundo(self):
        retangulo = Image.new("RGBA", (26, 18), (0, 0, 0, 0))
        draw = ImageDraw.Draw(retangulo)
        draw.rounded_rectangle(((0, 0), (26, 18)), radius = self.radius, fill = self.fill)
        self.imagem.paste(retangulo, (82, 3), mask=retangulo)

    def Adicionar_amizade_fundo(self):
        retangulo = Image.new("RGBA", (43, 21), (0, 0, 0, 0))
        draw = ImageDraw.Draw(retangulo)
        draw.rounded_rectangle(((0, 0), (43, 21)), radius = self.radius, fill = self.fill)
        imagem_amizade = Image.open("imagens_base/amizade_level.png").resize((17, 15)).convert("RGBA")
        retangulo.paste(imagem_amizade, (4, 3), mask=imagem_amizade)
        self.imagem.paste(retangulo, (65, 87), mask=retangulo)

    def Adicionar_nivel_fundo(self):
        retangulo = Image.new("RGBA", (48, 21), (0, 0, 0, 0))
        draw = ImageDraw.Draw(retangulo)
        draw.rounded_rectangle(((0, 0), (48, 21)), radius = self.radius, fill = self.fill)
        self.imagem.paste(retangulo, (2, 87), mask=retangulo)
    