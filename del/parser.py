import os
from dotenv import load_dotenv
from telethon import TelegramClient

from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"

#print("Route to .env:", env_path)
#print("File exists:", env_path.exists())

load_dotenv(env_path)

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

#print("API ID found:", api_id is not None)
#print("API Hash found:", api_hash is not None)

#print("API ID not empty:", bool(api_id and api_id.strip()))
#print("API Hash not empty:", bool(api_hash and api_hash.strip()))

if not api_id or not api_hash:
    raise ValueError("Error getting data from .env")

api_id = int(api_id.strip())
api_hash = api_hash.strip()

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    
    channel_username = 'bbcukrainian' 

    async for message in client.iter_messages(channel_username, limit=5):
        if message.text:
            print(f"ID: {message.id} | Дата: {message.date}")
            print(f"Текст: {message.text[:100]}...\n" + "-"*40)

with client:
    client.loop.run_until_complete(main())