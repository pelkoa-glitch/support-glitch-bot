from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseCharService(ABC):
    @abstractmethod
    async def set_current_chat(self, chat_oid: str, telegram_chat_id: str) -> None:
        ...


@dataclass
class MongoDBChatService(ABC):
    async def set_current_chat(self, chat_oid: str, telegram_chat_id: str) -> None:
        ...
