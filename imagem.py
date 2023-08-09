import PIL
from disnake import File
from PIL import Image, ImageDraw
import io
import urllib.request
import os
from math import ceil

def Construir_imagem_personagens(personagens):
    largura_imagem = 1390
    altura_imagem = 328 + ceil(len(personagens) / 11) * 140
    imagem_fundo = Image.new(mode="RGBA", 
                             size=(largura_imagem, altura_imagem),
                             color="#3d4754")
    
    # linha maior
    draw = ImageDraw.Draw(imagem_fundo)
    draw.rounded_rectangle([(5, 5), (largura_imagem - 5, altura_imagem - 5)],
                   outline="#ffd4c1", fill=None, radius=50,width=5)
    
    # linha menor
    draw.rounded_rectangle([(19, 19), (largura_imagem - 19, altura_imagem - 19)],
                   outline="#9e8e8b", fill=None, radius=40,width=4)


    posicao_y = 0
    for pos, personagem in enumerate(personagens):
        imagem_personagem = Construir_icone_personagem(personagem)

        if pos % 11 == 0 and pos != 0:
            posicao_y += 1

        imagem_fundo.paste(imagem_personagem, 
                           ((110 + 10) * (pos % 11) + 40, 
                            posicao_y * (133 + 7) + 100),
                            mask=imagem_personagem)

    image_buffer = io.BytesIO()
    imagem_fundo.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    arquivo = File(image_buffer, filename='image.png')
    image_buffer.close()
    return arquivo


def Construir_icone_personagem(personagem):
    caminho_imagem = "imagens/icone_" + personagem["name"].lower().replace(" ", "_") + ".png"

    if not os.path.isfile(caminho_imagem):
        urllib.request.urlretrieve(personagem["icon"], caminho_imagem)
        imagem_personagem_novo = Image.open(caminho_imagem).resize((110, 110))
        raridade = personagem["rarity"]
        if personagem["name"] == "Aloy":
            raridade = 3
        caminho_imagem_fundo = "imagens/fundo_" + str(raridade) + "_estrelas.png"
        imagem_fundo_personagem = Image.open(caminho_imagem_fundo)
        imagem_fundo_personagem.paste(imagem_personagem_novo, mask=imagem_personagem_novo)
        imagem_fundo_personagem.save(caminho_imagem)

    imagem_personagem = Image.open(caminho_imagem)
    return imagem_personagem
