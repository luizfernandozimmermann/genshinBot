import genshin


class GenshinServico():
    async def get_genshin_user(ltuid : int, ltoken : str, uid: int):
        cookies = {"ltuid": ltuid, "ltoken": ltoken}
        client = genshin.Client(cookies)

        data = await client.get_genshin_user(uid)
        return data
