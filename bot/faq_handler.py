from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async

from api.user.models import FAQQuestion

faq_router = Router()

@sync_to_async
def get_all_faq_questions():
    """Get all FAQ questions from the database."""
    return list(FAQQuestion.objects.all())

@faq_router.callback_query(F.data == 'faq')
async def faq_start(callback: types.CallbackQuery, state: FSMContext):
    """Display the list of FAQ questions."""
    await state.clear()
    questions = await get_all_faq_questions()
    
    kb = InlineKeyboardBuilder()
    for question in questions:
        kb.button(text=question.question, callback_data=f'faq_question_{question.id}')
    kb.button(text='◀️ Назад', callback_data='main_menu')
    kb.adjust(1)  # One button per row
    
    await callback.message.edit_text("Выберите вопрос:", reply_markup=kb.as_markup())

@faq_router.callback_query(F.data.startswith('faq_question'))
async def faq_question_selected(callback: types.CallbackQuery):
    """Display the answer to the selected question."""
    question_id = int(callback.data.split('_')[-1])

    @sync_to_async
    def get_faq_question(question_id):
        return FAQQuestion.objects.get(id=question_id)

    question = await get_faq_question(question_id)
    kb = InlineKeyboardBuilder()
    kb.button(text='◀️ Назад к вопросам', callback_data='faq_menu')
    
    await callback.message.edit_text(
        f"<b>{question.question}</b>\n\n{question.answer}",
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )

@faq_router.callback_query(F.data == 'faq_menu')
async def faq_menu(callback: types.CallbackQuery):
    """Display the list of FAQ questions."""
    questions = await get_all_faq_questions()
    
    kb = InlineKeyboardBuilder()
    for question in questions:
        kb.button(text=question.question, callback_data=f'faq_question_{question.id}')
    kb.button(text='◀️ Назад', callback_data='main_menu')
    kb.adjust(1)  # One button per row
    
    await callback.message.edit_text("Выберите вопрос:", reply_markup=kb.as_markup())


