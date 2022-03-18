import asyncio
import os

from pyrogram import Client

PYROGRAM_SESSION_FILE: os.path = input("Please insert path to pyrogram session file: ")
API_ID: int = int(input("Please insert session api id: "))
API_HASH: str = input("Please insert session api hash: ")
TG_USERNAME_RECIPIENT: str = input(
    "Please insert telegram username recipient for test message: "
)


async def check_pyro():
    async with Client(PYROGRAM_SESSION_FILE, api_id=API_ID, api_hash=API_HASH) as app:
        await app.send_message(TG_USERNAME_RECIPIENT, "Client success work!")


if __name__ == "__main__":
    asyncio.run(check_pyro())
