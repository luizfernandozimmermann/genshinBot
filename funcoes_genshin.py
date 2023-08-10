import genshin

async def get_characters(ltuid : int, ltoken : str, uid: int):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies)

    data = await client.get_genshin_characters(uid)
    return data