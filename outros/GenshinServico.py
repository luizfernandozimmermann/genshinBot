import genshin


class GenshinServico():
    async def get_genshin_user(cookies : dict, uid: int):
        client = genshin.Client(cookies)

        data = await client.get_genshin_user(uid)
        return data
    
    async def checar_usuario_valido(cookies : dict, uid : int):
        try:
            client = genshin.Client(cookies)
            await client.get_genshin_user(uid)
            return True
        except:
            return False
