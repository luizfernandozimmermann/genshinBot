import genshin


async def get_full_user_info(ltuid : int, ltoken : str, uid: int):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies)

    data = await client.get_full_genshin_user(uid)
    return data
