from dataclasses import dataclass

from dtos.chats import ChatInfoDTO
from repositories.chats.base import BaseChatsRepository



@dataclass(eq=False)
class ChatsService:
    repository: BaseChatsRepository

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        return await self.repository.add_chat(chat_info=chat_info)
