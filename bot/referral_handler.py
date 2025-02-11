from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_bot_text, identify_user
from api.user.models import Refer, User, Subscription, SubscriptionDetails
from asgiref.sync import sync_to_async
from datetime import timedelta

referral_router = Router()

@sync_to_async
def get_referrals(user: User, bought: bool = None):
    query = Refer.objects.filter(refer_user=user)
    if bought is not None:
        query = query.filter(bought=bought)
    return list(query.select_related('invited_user'))

@sync_to_async
def add_subscription_reward(user: User):
    # Get 1-week subscription type
    subs_type = SubscriptionDetails.objects.get(id=1)
    
    # Check if user has active subscription
    current_sub = Subscription.objects.filter(user=user).first()
    
    if current_sub:
        # Add days to existing subscription
        current_sub.date_of_creation += timedelta(days=7)
        current_sub.save()
    else:
        # Create new subscription
        Subscription.objects.create(
            user=user,
            subscription_type=subs_type
        )

@referral_router.callback_query(F.data == 'referral_program')
async def referral_program_handler(call: CallbackQuery):
    user, _ = await identify_user(call)
    
    bot_info = await call.bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start={user.username}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Приглашенные вами люди", callback_data="invited_users")],
        [InlineKeyboardButton(text="💰 Купившие люди", callback_data="bought_users")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])
    
    await call.message.edit_text(
        text=f"🔗 Ваша реферальная ссылка:\n{referral_link}\n\n"
             f"Приглашайте друзей и получайте бонусы!\n"
             f"За каждого купившего друга вы получите 7 дней подписки.",
        reply_markup=keyboard
    )
    
    await call.answer()

@referral_router.callback_query(F.data == 'invited_users')
async def invited_users_handler(call: CallbackQuery):
    user, _ = await identify_user(call)
    
    referrals = await get_referrals(user)
    
    text = "👥 Приглашенные вами пользователи:\n\n"
    if not referrals:
        text += "Пока никого нет"
    else:
        for ref in referrals:
            status = "✅ Купил" if ref.bought else "❌ Не купил"
            text += f"<a href='tg://user?id={ref.invited_user.username}'>{ref.invited_user.first_name}</a> - {status}\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="referral_program")]
    ])
    
    await call.message.edit_text(text=text, reply_markup=keyboard)
    await call.answer()

@referral_router.callback_query(F.data == 'bought_users')
async def bought_users_handler(call: CallbackQuery):
    user, _ = await identify_user(call)
    
    bought_referrals = await get_referrals(user, bought=True)
    
    text = "💰 Пользователи, совершившие покупку:\n\n"
    if not bought_referrals:
        text += "Пока никого нет"
    else:
        for ref in bought_referrals:
            text += f"@{ref.invited_user.username}\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="referral_program")]
    ])
    
    await call.message.edit_text(text=text, reply_markup=keyboard)
    await call.answer() 