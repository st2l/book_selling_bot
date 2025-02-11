from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_bot_text, identify_user

like_minded_chat_router = Router()

@like_minded_chat_router.callback_query(F.data == 'like_minded_chat')
async def like_minded_chat_handler(call: CallbackQuery):
    user, _ = await identify_user(call)
    
    chat_text = await get_bot_text(name='Текст для чата единомышленников')
    chat_link = await get_bot_text(name='Ссылка для чата единомышленников')
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Присоединиться к чату", url=chat_link)],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])
    
    await call.message.edit_text(
        text=chat_text,
        reply_markup=keyboard
    )
    
    await call.answer() 