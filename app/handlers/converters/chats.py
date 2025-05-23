from dtos.chats import ChatListItemDTO


def convert_chats_dtos_to_message(chats: list[ChatListItemDTO]) -> str:
    return '\n\n'.join(
        (
            f'Список всех доступных чатов:',
            '\n\n'.join(
                (rf'ChatOID: `{chat.oid}`\. Проблема: {chat.title}' for chat in chats)
            ),
        )
    )
