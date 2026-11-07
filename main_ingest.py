import os
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from db import get_or_create_channel, save_post


load_dotenv(Path(__file__).resolve().parent / ".env")

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")

client = TelegramClient('session_name', api_id, api_hash)

async def process_channel(target_channel):
    entity = await client.get_entity(target_channel)
    channel_title = entity.title or target_channel
    
    print(f"Processing channel: {channel_title} (@{target_channel})")

    channel_id = get_or_create_channel(target_channel, channel_title)
    
    saved_count = 0
    skipped_count = 0

    
    async for message in client.iter_messages(target_channel, limit=100):
        if not message.text:
            continue

        telegram_post_id = message.id
        text = message.text
        views = message.views or 0
        published_at = message.date

        is_saved = save_post(
            channel_id=channel_id,
            telegram_post_id=telegram_post_id,
            text=text,
            views=views,
            published_at=published_at
        )
        
        if is_saved:
            saved_count += 1
        else:
            skipped_count += 1

    print(f"Done. New posts added: {saved_count}, Duplicates skipped: {skipped_count}\n")

async def main():
    channels_to_parse = [
        'u_now',
        'UaOnlii',
        'truexanewsua',
        'lachentyt',
        'bbcukrainian',
        'TCH_channel',
        'channel24_ua',
        'novynylive',
        'ukraina_novosti',
        'signal_ukraine',
        'censor_net',
        'ukrinform_news'

    ]
    
    for channel in channels_to_parse:
        try:
            await process_channel(channel)
        except Exception as e:
            print(f"Error while processing {channel}: {e}")

with client:
    client.loop.run_until_complete(main())