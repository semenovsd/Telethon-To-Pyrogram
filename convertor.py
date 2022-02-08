import asyncio
import base64
import os
import sqlite3
import struct
from pathlib import Path
from typing import Union

from pyrogram import Client
from pyrogram.storage import Storage, FileStorage
from telethon import TelegramClient

from telethon.sessions import StringSession
from telethon.tl import types


# Remember to use your own values from my.telegram.org!
SESSION_NAME: str = input("Please insert telethon session file, e.g. +79212121212: ")
API_ID: int = int(input("Please insert session api id: "))
API_HASH: str = input("Please insert session api hash: ")

BASE_DIR: os.path = Path(__file__).resolve().parent

# Insert path to telethon session dir
TELETHON_SESSION_DIR: os.path = os.path.join(BASE_DIR, 'telethon/')
TELETHON_SESSION_FILE: os.path = os.path.join(TELETHON_SESSION_DIR, f'{SESSION_NAME}.session')

# Insert path to pyrogram session dir
PYROGRAM_SESSION_DIR: os.path = os.path.join(BASE_DIR, 'pyrogram/')
PYROGRAM_SESSION_FILE: os.path = os.path.join(PYROGRAM_SESSION_DIR, f'{SESSION_NAME}.session')


def pack_to_pyro(data: StringSession, ses: types.User):
    return base64.urlsafe_b64encode(
        struct.pack(
            Storage.SESSION_STRING_FORMAT,
            data.dc_id,
            None,
            data.auth_key.key,
            ses.id,
            ses.bot
        )).decode().rstrip("=")


async def main():
    # The first parameter is the .session file name (absolute paths allowed)
    async with TelegramClient(TELETHON_SESSION_FILE, API_ID, API_HASH) as client:
        # Getting information about yourself
        me: Union[types.User, types.InputPeerUser] = await client.get_me()
        session_string = StringSession.save(client.session)
        data = StringSession(session_string)
        pyro_session_string = pack_to_pyro(data, me)

    async with Client(pyro_session_string, api_id=API_ID, api_hash=API_HASH,
                      workdir=PYROGRAM_SESSION_DIR) as app:
        file_storage = FileStorage(SESSION_NAME, Path(PYROGRAM_SESSION_DIR))
        file_storage.conn = sqlite3.Connection(PYROGRAM_SESSION_FILE)

        app.storage = file_storage
        app.storage.create()

        await file_storage.dc_id(data.dc_id)
        await file_storage.test_mode(False)
        await file_storage.auth_key(data.auth_key.key)
        await file_storage.user_id(me.id)
        await file_storage.date(0)
        await file_storage.is_bot(False)

        await app.storage.save()

        print(f'Session success converted and saved to {PYROGRAM_SESSION_FILE}')


if __name__ == '__main__':
    asyncio.run(main())
