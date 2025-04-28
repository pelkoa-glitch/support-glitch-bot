from faststream import Context
from faststream.kafka import KafkaRouter
from telegram import Bot

from consumers.schemas import NewChatMessageSchema, NewChatSchema
from containers.factories import get_container
from services.web import BaseChatWebService
from settings import get_settings


router = KafkaRouter()
settings = get_settings()


@router.subscriber(settings.NEW_MESSAGE_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_chat_handler(message: NewChatSchema) -> None:
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        await bot.create_forum_topic


@router.subscriber(settings.NEW_MESSAGE_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_message_subscription_handler(
    message: NewChatMessageSchema, key: bytes = Context("message.raw_message.key")
) -> None:
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        listeners = await service.get_chat_listeners(chat_oid=key.decode())
        chat_info = await service.get_chat_info(chat_oid=key.decode())

        bot = await request_container.get(Bot)

        for listener in listeners:
            await bot.send_message(
                chat_id=listener.oid,
                text=(
                    f"Сообщение из чата (<code>{chat_info.oid}</code>) <b>{chat_info.title}</b>"
                    f"<blockquote>{message.message_text}</blockquote>"
                ),
                parse_mode="HTML",
            )
