from typing import Tuple

from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model 
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from conf.settings import MIDDLEWARE


User = get_user_model()

def platform_access(update: Update, context: CallbackContext) -> str:
    '''Предоставление доступа на платформу'''
    chat_id = update.message.chat_id
    tg_user_id = update.message.from_user.id
    tg_username = update.message.from_user.username
    if tg_username:
        msg, reply_markup  = _telegram_authentication(tg_user_id, tg_username)
        return msg, reply_markup 
    return 'Нужно сделать юзернейм', None


def _telegram_authentication(user_id: int, username: str) -> Tuple[str, str]:
    user, created = User.objects.get_or_create(
                    tg_id=user_id, 
                    defaults={'username': username,'tg_username': username}
                    )
    return _create_message_and_link(user, created)


def _create_message_and_link(user, created):
    if created:
        begin_msg = f'Привет @{user.username} !\nЗарегистрироваться в Среде можно здесь:\n\n'
        btn_msg = 'Пройти регистрацию'
    else:
        begin_msg = f'Привет @{user.username} !\nЗалогиниться в Среде можно здесь:\n\n'
        btn_msg = 'Войти в Среду'
    link = _create_registration_link(user)
    end_msg = '\n\nСсылка будет активна минуту, чтобы ее обновить - отправьте, например, /start \nЛибо любое сообщение, если хотите с нами чем-то поделиться...\nМы читаем каждое сообщение!'
    
    msg = begin_msg + link + end_msg
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text=btn_msg, url=link)]
    ])

    return msg, reply_markup

def _create_registration_link(user: User) -> str:
    '''Создает уникальнкую ссылку для прохождения регистрации'''
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    link = 'http://127.0.0.1:8000/' + 'users/' + f'sing_up/{uidb64}/{token}'
    return link


def get_user_and_check_token(uidb64, token):
    '''Достает пользователя и проверяет токен'''
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        check_token = token_generator.check_token(user, token)
    except(
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
        ValidationError,
        ):
        user = None
        check_token = False
    return user, check_token