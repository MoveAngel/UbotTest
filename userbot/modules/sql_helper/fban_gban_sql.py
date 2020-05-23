from userbot import MONGO, REDIS

# Fbans


async def get_fban():
    return MONGO.fban.find()


async def add_chat_fban(chatid):
    if await is_fban(chatid) is True:
        return False
    else:
        MONGO.fban.insert_one({'chatid': chatid})


async def remove_chat_fban(chatid):
    if await is_fban(chatid) is False:
        return False
    else:
        MONGO.fban.delete_one({'chatid': chatid})
        return True


async def is_fban(chatid):
    if not MONGO.fban.find_one({"chatid": chatid}):
        print("FAILED on fed")
        return False
    else:
        return True


# Gbans


async def get_gban():
    return MONGO.gban.find()


async def add_chat_gban(chatid):
    if await is_gban(chatid) is True:
        print("FAILED")
        return False
    else:
        MONGO.gban.insert_one({'chatid': chatid})


async def remove_chat_gban(chatid):
    if await is_gban(chatid) is False:
        return False
    else:
        MONGO.gban.delete_one({'chatid': chatid})
        return True


async def is_gban(chatid):
    if not MONGO.gban.find_one({"chatid": chatid}):
        return False
    else:
        return True
