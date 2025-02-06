from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext  
from asgiref.sync import sync_to_async
from api.user.models import DialogResponse, DialogTask, User
from utils import identify_user
from aiogram.fsm.state import State, StatesGroup
import logging

dialog_router = Router()

@sync_to_async
def create_dialog_response(user: User, task_id: int, dialog_answer: str):
    try:
        task = DialogTask.objects.get(id=task_id)
    except DialogTask.DoesNotExist:
        logging.error(f'Dialog task not found: {task_id}')
        return None
    
    return DialogResponse.objects.create(
        user=user,
        dialog_task=task,
        response_text=dialog_answer
    )

class DialogStates(StatesGroup):
    dialog_answer = State()

@dialog_router.callback_query(F.data.startswith('dialog_answer_'))
async def handle_dialog_response(call: CallbackQuery, state: FSMContext):
    user, _ = await identify_user(call)
    
    task_id = call.data.split('_')[-1]
    await state.update_data(task_id=task_id)
    await state.set_state(DialogStates.dialog_answer)

    await call.message.answer(
        text=f'Введите ваш ответ на задание!'
    )
    
    await call.answer()

@dialog_router.message(DialogStates.dialog_answer)
async def process_dialog_answer(message: Message, state: FSMContext):
    await state.update_data(dialog_answer=message.text)

    data = await state.get_data()
    task_id = data.get('task_id')

    logging.info(f'Dialog answer: {message.text}\ntask_id: {task_id}')

    await state.clear()
    user, _ = await identify_user(message)
    
    await create_dialog_response(user, task_id, message.text)

    await message.answer(
        text=f'Спасибо за ваш ответ!',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Вернуться в ЛК', callback_data='user_lk')]
            ]
        )
    )
