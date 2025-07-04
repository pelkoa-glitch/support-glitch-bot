from faststream.kafka import KafkaRouter
from telegram import Bot

from consumers.schemas import DeleteChatSchema, NewChatMessageSchema, NewChatSchema
from containers.factories import get_container
from services.chats import ChatsService
from settings import get_settings


router = KafkaRouter()
settings = get_settings()


@router.subscriber(settings.NEW_CHAT_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_chat_handler(data: NewChatSchema) -> None:
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        chat = await bot.get_chat(chat_id=settings.TELEGRAM_GROUP_ID)
        chats_service = await request_container.get(ChatsService)

        topic_title = data.chat_title
        topic = await chat.create_forum_topic(name=topic_title)
        await chats_service.add_chat(
            web_chat_id=data.chat_oid,
            telegram_chat_id=str(topic.message_thread_id)
        )

@router.subscriber(settings.NEW_MESSAGE_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_message_handler(
    message: NewChatMessageSchema
) -> None:
    container = get_container()

    async with container() as request_container:
        chats_service = await request_container.get(ChatsService)
        chat_info = await chats_service.get_chat_info_by_web_chat_id(web_chat_id=message.chat_oid)

        bot = await request_container.get(Bot)
        chat = await bot.get_chat(chat_id=settings.TELEGRAM_GROUP_ID)
        if message.is_manager == False:
            await chat.send_message(
                text=message.message_text,
                message_thread_id=int(chat_info.telegram_chat_id)
            )

@router.subscriber(settings.DELETE_CHAT_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def delete_chat_handler(data: DeleteChatSchema) -> None:
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        chat = await bot.get_chat(chat_id=settings.TELEGRAM_GROUP_ID)
        chats_service = await request_container.get(ChatsService)

        chat_info = await chats_service.get_chat_info_by_web_chat_id(web_chat_id=data.chat_oid)

        await chats_service.delete_chat(web_chat_id=data.chat_oid)
        await chat.delete_forum_topic(message_thread_id=int(chat_info.telegram_chat_id))
