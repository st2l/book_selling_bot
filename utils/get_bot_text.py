from api.user.models import BotText


async def get_bot_text(name: str) -> str:
    bot_text = await BotText.objects.aget(name=name)
    return bot_text.text
