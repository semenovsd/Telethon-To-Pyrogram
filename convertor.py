import asyncio
import base64
import os
import sqlite3
import struct
from argparse import Namespace
from pathlib import Path
from typing import Union

from pyrogram import Client
from pyrogram.storage import FileStorage, Storage
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl import types

from utils.args import parse_args


def pack_to_string(session_data: StringSession, user_data: types.User) -> str:
    try:
        bytes_result: bytes = struct.pack(
            Storage.SESSION_STRING_FORMAT,
            session_data.dc_id,
            None,
            session_data.auth_key.key,
            user_data.id,
            user_data.bot
        )
    except struct.error:
        bytes_result: bytes = struct.pack(
            Storage.SESSION_STRING_FORMAT_64,
            session_data.dc_id,
            None,
            session_data.auth_key.key,
            user_data.id,
            user_data.bot
        )
    encode_result: bytes = base64.urlsafe_b64encode(bytes_result)
    decode_result: str = encode_result.decode()
    result: str = decode_result.rstrip("=")
    return result


async def get_user_data(client: TelegramClient) -> Union[types.User, types.InputPeerUser]:
    user_data = await client.get_me()
    return user_data


async def get_session_data(client: TelegramClient) -> StringSession:
    session_string = StringSession.save(client.session)
    session_data = StringSession(session_string)
    return session_data


async def save_pyro_session(client: Client, session_data: StringSession):
    user_data = await client.get_me()
    await client.storage.dc_id(session_data.dc_id)
    await client.storage.test_mode(False)
    await client.storage.auth_key(session_data.auth_key.key)
    await client.storage.user_id(user_data.id)
    await client.storage.date(0)
    await client.storage.is_bot(False)
    # Save session
    await client.storage.save()


async def convert(params: Namespace):
    params.pyro_session_file = os.path.join(params.pyro_session_dir, os.path.basename(params.telethon_session_file))
    if os.path.exists(params.pyro_session_file):
        # os.remove(params.pyro_session_file)
        raise FileExistsError(f'File {params.pyro_session_file} already exist!')
    params.pyro_session_name = os.path.splitext(os.path.basename(params.telethon_session_file))[0]

    # The first parameter is the .session file name (absolute paths allowed)
    async with TelegramClient(params.telethon_session_file, params.api_id, params.api_hash) as client:
        # Getting information about yourself
        user_data = await get_user_data(client)
        # Getting session information
        session_data = await get_session_data(client)
    # Convert session data to pyrogram session string
    session_string = pack_to_string(session_data, user_data)

    async with Client(session_string,
                      api_id=params.api_id,
                      api_hash=params.api_hash,
                      workdir=params.pyro_session_dir) as client:
        client.storage = FileStorage(params.pyro_session_name, Path(params.pyro_session_dir))
        client.storage.conn = sqlite3.Connection(params.pyro_session_file)  # sqlite3.OperationalError: not exist
        client.storage.create()  # sqlite3.OperationalError: already exists
        await save_pyro_session(client, session_data)
    print(f'Session success converted and saved to {params.pyro_session_file}')


def get_session_files(session_dir: str) -> list:
    session_files = [os.path.join(session_dir, x) for x in os.listdir(session_dir) if x.endswith('.session')]
    if len(session_files) == 0:
        raise FileNotFoundError(f'Session files does not found in {session_dir}.')
    return session_files


async def start(params: Namespace):
    if params.telethon_session_file and params.telethon_session_dir:
        raise OSError('Please set only one of -f [path/to/file.session] or -d [path/to/sessions/].')
    if not params.telethon_session_file and not params.telethon_session_dir:
        raise OSError('Please set -f [path/to/file.session] or -d [path/to/sessions/].')
    if params.telethon_session_file and not os.path.isfile(params.telethon_session_file):
        raise FileNotFoundError('Session file does not exist. Please check path to Telethon session file.')
    if params.telethon_session_dir and not os.path.isdir(params.telethon_session_dir):
        raise NotADirectoryError('Please check path to Telethon session dir. Works only on directories.')

    if not params.api_id:
        params.api_id = int(input("Please insert API ID from https://my.telegram.org/apps:"))
    if not params.api_hash:
        params.api_hash = input("Please insert API HASH from https://my.telegram.org/apps:")

    if not os.path.exists(params.pyro_session_dir):
        os.mkdir(params.pyro_session_dir)

    if params.telethon_session_dir:
        files = get_session_files(params.telethon_session_dir)
    else:
        files = [params.telethon_session_file]

    for file in files:
        params.telethon_session_file = file
        await convert(params)


if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(start(args))
    except KeyboardInterrupt:
        pass
