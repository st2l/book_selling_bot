from api.user.models import BotText


async def get_bot_text(name: str) -> str:
    try:
        bot_text = await BotText.objects.aget(name=name)
    except:
        bot_text = await BotText.objects.acreate(name=name, text='тестовый текст.')
    return bot_text.text
