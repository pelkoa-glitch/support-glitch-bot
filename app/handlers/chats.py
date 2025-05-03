import logging
import re
from telegram import Bot, Update
from telegram.ext import ContextTypes

from containers.factories import get_container
from handlers.constants import SEND_MESSAGE_STATE
from handlers.converters.chats import convert_chats_dtos_to_message
from services.chats import ChatsService
from services.web import BaseChatWebService


async def get_all_chats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        chats = await service.get_all_chats()

        await context.bot.send_message(
            chat_id=update.effective_chat.id, # type: ignore
            text=convert_chats_dtos_to_message(chats=chats),
            parse_mode='MarkdownV2',
        )


async def set_chat_listener_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        await service.add_listener(
            telegram_chat_id=update.effective_chat.id, # type: ignore
            chat_oid=context.args[0], # type: ignore
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id, # type: ignore
            text='Вы подключились к чату.',
            parse_mode='MarkdownV2',
        )


async def quit_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text='Вы вышли из чата.',
        parse_mode='MarkdownV2',
    )


async def start_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text=(
            'Теперь вы отвечаете на сообщения. Выберите сообщение и '
            'напишите ответ. Пользователь увидит ваш ответ на сайте.'
        ),
    )

    return SEND_MESSAGE_STATE


async def send_message_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        web_service = await request_container.get(BaseChatWebService)
        service = await request_container.get(ChatsService)
        chat_info = await service.get_chat_info_by_telegram_id(telegram_chat_id=update.message.message_thread_id) # type: ignore

        await web_service.send_message_to_chat(chat_oid=chat_info.web_chat_id, message_text=update.message.text) # type: ignore
