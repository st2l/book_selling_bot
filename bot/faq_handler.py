from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

from api.user.models import FAQQuestion

faq_router = Router()

@sync_to_async
def get_all_faq_questions():
    """Get all FAQ questions from the database."""
    return list(FAQQuestion.objects.all())

@faq_router.callback_query(F.data == 'faq')
async def faq_start(message: types.Message, state: FSMContext):
    """Display the list of FAQ questions."""
    await state.finish()
    questions = await get_all_faq_questions()
    keyboard = InlineKeyboardMarkup(row_width=1)
    for question in questions:
        keyboard.add(InlineKeyboardButton(
            text=question.question, callback_data=f'faq_question_{question.id}'))
        
    keyboard.add(InlineKeyboardButton(text='◀️ Назад', callback_data='main_menu'))
    await message.answer("Выберите вопрос:", reply_markup=keyboard)

@faq_router.callback_query(F.data.startswith('faq_question'))
async def faq_question_selected(query: types.CallbackQuery):
    """Display the answer to the selected question."""
    question_id = int(query.data.split('_')[-1])

    @sync_to_async
    def get_faq_question(question_id):
        return FAQQuestion.objects.get(id=question_id)

    question = await get_faq_question(question_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='◀️ Назад к вопросам', callback_data='faq_menu'))
    await query.message.edit_text(f"<b>{question.question}</b>\n\n{question.answer}",
                                  reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


@faq_router.callback_query(F.data == 'faq_menu')
async def faq_menu(query: types.CallbackQuery):
    """Display the list of FAQ questions."""
    questions = await get_all_faq_questions()
    keyboard = InlineKeyboardMarkup(row_width=1)
    for question in questions:
        keyboard.add(InlineKeyboardButton(
            text=question.question, callback_data=f'faq_question_{question.id}'))
    keyboard.add(InlineKeyboardButton(text='◀️ Назад', callback_data='main_menu'))
    await query.message.edit_text("Выберите вопрос:", reply_markup=keyboard)


