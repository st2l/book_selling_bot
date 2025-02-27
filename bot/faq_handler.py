from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from utils import get_bot_text

from api.user.models import FAQQuestion

faq_router = Router()

@sync_to_async
def get_all_faq_questions():
    """Get all FAQ questions from the database."""
    return list(FAQQuestion.objects.all())

def get_faq_keyboard(questions, current_page: int = 0, items_per_page: int = 5):
    """Create a keyboard with pagination for FAQ questions."""
    kb = InlineKeyboardBuilder()
    
    # Calculate pagination
    total_pages = (len(questions) - 1) // items_per_page + 1
    start_idx = current_page * items_per_page
    end_idx = start_idx + items_per_page
    
    # Add question buttons for current page
    for question in questions[start_idx:end_idx]:
        kb.button(text=question.question, callback_data=f'faq_question_{question.id}')
    
    # Add navigation buttons
    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️", callback_data=f'faq_page_{current_page-1}'))
    
    if current_page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="➡️", callback_data=f'faq_page_{current_page+1}'))
    
    kb.adjust(1)  # One question per row
    if nav_buttons:
        kb.row(*nav_buttons)  # Add navigation buttons in one row
    
    kb.row([InlineKeyboardButton(text='🔙 Назад', callback_data='main_menu')])
    return kb.as_markup()

@faq_router.callback_query(F.data == 'faq')
async def faq_start(callback: types.CallbackQuery, state: FSMContext):
    """Display the first page of FAQ questions."""
    await state.clear()
    questions = await get_all_faq_questions()
    keyboard = get_faq_keyboard(questions, current_page=0)
    await callback.message.edit_text(
        await get_bot_text('Текст для FAQ'),
        reply_markup=keyboard
    )

@faq_router.callback_query(F.data.startswith('faq_page_'))
async def faq_page(callback: types.CallbackQuery):
    """Handle pagination."""
    page = int(callback.data.split('_')[-1])
    questions = await get_all_faq_questions()
    keyboard = get_faq_keyboard(questions, current_page=page)
    await callback.message.edit_text(
        await get_bot_text('Текст для FAQ'),
        reply_markup=keyboard
    )

@faq_router.callback_query(F.data.startswith('faq_question'))
async def faq_question_selected(callback: types.CallbackQuery):
    """Display the answer to the selected question."""
    question_id = int(callback.data.split('_')[-1])

    @sync_to_async
    def get_faq_question(question_id):
        return FAQQuestion.objects.get(id=question_id)

    question = await get_faq_question(question_id)
    kb = InlineKeyboardBuilder()
    kb.button(text='◀️ Назад к вопросам', callback_data='faq')
    
    await callback.message.edit_text(
        f"<b>{question.question}</b>\n\n{question.answer}",
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )


