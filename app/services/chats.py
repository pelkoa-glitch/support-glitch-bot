from dataclasses import dataclass

from dtos.chats import ChatInfoDTO
from exceptions.chats import ChatAlredyExistsError, ChatNotFoundByTelegramIdError
from repositories.chats.base import BaseChatsRepository



@dataclass(eq=False)
class ChatsService:
    repository: BaseChatsRepository

    async def add_chat(self, telegram_chat_id: str, web_chat_id: str) -> ChatInfoDTO:
        if await self.repository.check_chat_exists(
            web_chat_id=web_chat_id,
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatAlredyExistsError(
                web_chat_id=web_chat_id,
                telegram_chat_id=telegram_chat_id,
            )

        return await self.repository.add_chat(chat_info=ChatInfoDTO(
            web_chat_id=web_chat_id,
            telegram_chat_id=telegram_chat_id
        ))


    async def get_chat_info_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        if not await self.repository.check_chat_exists(
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatNotFoundByTelegramIdError(
                telegram_chat_id=telegram_chat_id,
            )

        return await self.repository.get_by_telegram_id(telegram_chat_id=telegram_chat_id)
