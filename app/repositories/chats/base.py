from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlite3 import connect

from dtos.chats import ChatInfoDTO
from repositories.sqls import ADD_NEW_CHAT_INFO


class BaseChatsRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        ...

    @abstractmethod
    async def get_by_external_id(self, external_chat_id: str) -> ChatInfoDTO:
        ...

    @abstractmethod
    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        ...


@dataclass(eq=False)
class SQLChatsRepositorty(BaseChatsRepository):
    database_url: str

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        async with connect(self.database_url) as connection:
            row = await connection.execute_insert(
                ADD_NEW_CHAT_INFO,
                (chat_info.web_chat_id, chat_info.telegram_chat_id)
            )
            web_chat_id, telegramchat_id = row

        return ChatInfoDTO(web_chat_id=web_chat_id, telegram_chat_id=telegramchat_id)
