from telegram import Update
from telegram.ext import CallbackContext

from exceptions.base import ApplicationException
from exceptions.chats import BaseWebException


async def error_handler(update: Update, context: CallbackContext) -> None:
    try:
        raise context.error # type: ignore
    except BaseWebException as error:
        await update.effective_message.reply_text( # type: ignore
            '\n'.join((error.message, error.error_text))
        )
    except ApplicationException as error:
        print(error.meta)
        await update.effective_message.reply_text(error.message) # type: ignore
