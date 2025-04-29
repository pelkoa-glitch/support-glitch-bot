CREATE_MAPPING_TABLE_SQL_QUERRY = '''
CREATE TABLE IF NOT EXISTS chat_web_mapping (
    web_chat_id INTEGER,
    telegram_chat_id INTEGER,
    PRIMARY KEY( web_chat_id, telegram_chat_id)
);
'''
ADD_NEW_CHAT_INFO = '''
'''
