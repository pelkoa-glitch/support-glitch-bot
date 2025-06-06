from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    GREETING_TEXT: str = Field(
        default=(
            'Добро пожаловать в бот техподдержки.\n'
            'Пожалуйста выберите чат для работы с клиентом.\nПолучить список всех чатов: '
            '/chats, выбрать чат /listen_chat <oid чата>.'
        ),
    )
    WEB_API_BASE_URL: str = Field(default='http://main-app:8000')
    KAFKA_BROKER_URL: str = Field(default='kafka:29092')
    NEW_MESSAGE_TOPIC: str = Field(default='new-messages')
    NEW_CHAT_TOPIC: str = Field(default='new-chats-topic')
    DELETE_CHAT_TOPIC: str = Field(default='chat-deleted-topic')
    KAFKA_GROUP_ID: str = Field(default='tg-bot')
    DATABASE_NAME: str = Field(default='sqlite.db')
    TELEGRAM_GROUP_ID: str = Field()
    TG_BOT_TOKEN: str = Field()


@lru_cache(1)
def get_settings() -> ProjectSettings:
    return ProjectSettings() # type: ignore
