import json

def salvar(conteudo, arquivo="usuarios"):
    with open(arquivo + ".json", "w", encoding='UTF-8') as saving:
        json.dump(conteudo, saving)

def carregar(arquivo="usuarios"):
    with open(arquivo + ".json", encoding='UTF-8') as loading:
        data = json.load(loading)
        return data