from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlite3 import DataError
from urllib.parse import urljoin
from httpx import AsyncClient, HTTPError, TimeoutException

from dtos.chats import ChatListItemDTO, ChatListenerDTO
from exceptions.chats import (
    ChatInfoRequestError,
    ChatListRequestError,
    ListenerAddRequestError,
    ListenerListRequestError,
    SendMessageFromTgToWebError,
)
from services.constants import (
    CHAT_INFO_URI,
    CHAT_LIST_URI,
    CHAT_LISTENERS_URI,
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    SEND_MESSAGE_TO_CHAT_URL,
)
from services.converters.chats import (
    convert_chat_listener_responce_to_dto,
    convert_chat_response_to_chat_dto,
)


@dataclass
class BaseChatWebService(ABC):
    http_client: AsyncClient
    base_url: str

    @abstractmethod
    async def get_all_chats(self) -> list[ChatListItemDTO]:
        ...

    @abstractmethod
    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]:
        ...

    @abstractmethod
    async def add_listener(self, telegram_chat_id: int, chat_oid: str) -> None:
        ...

    @abstractmethod
    async def get_chat_info(self, chat_oid: str) -> ChatListItemDTO:
        ...
    @abstractmethod
    async def send_message_to_chat(self, chat_oid: str, message_text: str, is_manager: bool) -> None:
        ...

@dataclass
class ChatWebService(BaseChatWebService):
    async def get_all_chats(self) -> list[ChatListItemDTO]:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_LIST_URI),
            params={'limit': DEFAULT_LIMIT, 'offset': DEFAULT_OFFSET},
        )

        if not response.is_success:
            raise ChatListRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

        json_data = response.json()
        return [
            convert_chat_response_to_chat_dto(chat_data=chat_data)
            for chat_data in json_data['items']
        ]

    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]:
        response = await self.http_client.get(
            url=urljoin(
                base=self.base_url, url=CHAT_LISTENERS_URI.format(chat_oid=chat_oid)
            )
        )

        if not response.is_success:
            raise ListenerListRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

        json_data = response.json()
        return [
            convert_chat_listener_responce_to_dto(listener_data=listener_data)
            for listener_data in json_data
        ]

    async def add_listener(self, telegram_chat_id: int, chat_oid: str) -> None:
        response = await self.http_client.post(
            url=urljoin(
                base=self.base_url, url=CHAT_LISTENERS_URI.format(chat_oid=chat_oid)
            ),
            json={'telegram_chat_id': str(telegram_chat_id)},
        )

        if not response.is_success:
            raise ListenerAddRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

    async def get_chat_info(self, chat_oid: str) -> ChatListItemDTO:
        response = await self.http_client.get(
            url=urljoin(
                base=self.base_url,
                url=CHAT_INFO_URI.format(chat_oid=chat_oid)
            ),
        )

        if not response.is_success:
            raise ChatInfoRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

        return convert_chat_response_to_chat_dto(chat_data=response.json())


    async def send_message_to_chat(self, chat_oid: str, message_text: str, is_manager: bool) -> None:
        try:
            response = await self.http_client.post(
                url=urljoin(
                    base=self.base_url,
                    url=SEND_MESSAGE_TO_CHAT_URL.format(chat_oid=chat_oid)
                ),
                json={
                    'text': message_text,
                    'is_manager': is_manager,
                }
            )
            response.raise_for_status()
        except(TimeoutException, HTTPError):
            raise SendMessageFromTgToWebError()
