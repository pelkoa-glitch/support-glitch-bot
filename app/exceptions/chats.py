from dataclasses import dataclass

from exceptions.base import ApplicationException, BaseWebException


@dataclass(frozen=True, eq=False)
class ChatListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось получить список всех чатов'


@dataclass(frozen=True, eq=False)
class ListenerListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось получить список всех слушателей чата'


@dataclass(frozen=True, eq=False)
class ListenerAddRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось добавить слушателя к чату'


@dataclass(frozen=True, eq=False)
class ChatInfoRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось получить информацию о чате'


@dataclass(frozen=True, eq=False)
class ChatInfoNotFoundError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return 'Не удалось найти такой чат'


@dataclass(frozen=True, eq=False)
class ChatAlredyExistsError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return 'Такой чат уже существует'


@dataclass(frozen=True, eq=False)
class ChatNotFoundError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return 'Чат для ответа не зарегистрирован в боте'


@dataclass(frozen=True, eq=False)
class SendMessageFromTgToWebError(ApplicationException):
    @property
    def message(self) -> str:
        return 'Не удалось отправить сообщение в чат'
