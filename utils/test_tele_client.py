import asyncio
import os

from telethon import TelegramClient

TELETHON_SESSION_FILE: os.path = input("Please insert path to telethon session file: ")
API_ID: int = int(input("Please insert session api id: "))
API_HASH: str = input("Please insert session api hash: ")
TG_USERNAME_RECIPIENT: str = input(
    "Please insert telegram username recipient fro test message: "
)


async def check_telethon():
    async with TelegramClient(
        TELETHON_SESSION_FILE, api_id=API_ID, api_hash=API_HASH
    ) as client:
        await client.send_message(TG_USERNAME_RECIPIENT, "Client success work!")


if __name__ == "__main__":
    asyncio.run(check_telethon())
