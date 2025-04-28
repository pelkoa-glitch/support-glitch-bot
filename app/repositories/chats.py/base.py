from abc import ABC, abstractmethod

from dtos.messages import ChatInfoDTO


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


class SQLChatsRepositorty(BaseChatsRepository):
    ...
