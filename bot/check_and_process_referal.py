from api.user.models import User, Refer, SubscriptionDetails, Subscription, SubscriptionRenewal
from asgiref.sync import sync_to_async
import logging

@sync_to_async
def referal_bought(user: User):
    try:
        referral = Refer.objects.get(invited_user=user, bought=False)
        referral.bought = True
        referral.save()
        return referral
    except Refer.DoesNotExist:
        return None

@sync_to_async
def add_subscription_reward(refer: Refer):
    # Get 1-week subscription type
    subs_type = SubscriptionDetails.objects.get(id=1)  # 1 week subscription
    is_subscribed = Subscription.objects.filter(user=refer.refer_user).exists()
    if not is_subscribed:
        Subscription.objects.create(
            user=refer.refer_user,
            subscription_type=subs_type
        )
        logging.info(f"User {refer.refer_user.username} is not subscribed. Giving 1 week reward.")
    else:
        logging.info(f"User {refer.refer_user.username} is already subscribed. Giving 1 week reward.")
        SubscriptionRenewal.objects.create(
            user=refer.refer_user,
            subscription_type=subs_type
        )

@sync_to_async
def get_referrer(user: User):
    try:
        return Refer.objects.filter(invited_user=user).first()
    except Refer.DoesNotExist:
        return None

async def check_and_process_referral(user: User):
    try:
        referrer = await get_referrer(user)
        if referrer and referrer.bought:
            return

        # Check if user is referred by another user
        referral = await referal_bought(user)

        # Give reward to referrer
        await add_subscription_reward(referral)
    except Refer.DoesNotExist:
        pass


