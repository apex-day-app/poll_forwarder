import asyncio
import os
from telethon import TelegramClient, events

API_ID = 35089639
API_HASH = '0c46a9a35e7db749b8a9b87b0bdb0aec'
PHONE = '+917599181164'
PASSWORD = '181164'

SOURCE_CH = ['ssc_crack_gk']
DEST_CH = 'toforwerd'

client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    await client.start(PHONE, password=PASSWORD)
    print("✅ Logged in")

    # पुराने polls
    async for msg in client.iter_messages(SOURCE_CH[0], limit=50):
        if msg.poll:
            await client.send_poll(
                DEST_CH,
                question=msg.poll.poll.question,
                answers=[a.text for a in msg.poll.poll.answers],
                is_quiz=True,
                correct_option_id=msg.poll.poll.correct_option_id,
                close_date=int(asyncio.get_event_loop().time()) + 60
            )
            print("Poll recreated")

    # नए polls के लिए listener
    @client.on(events.NewMessage(chats=SOURCE_CH))
    async def forward(event):
        if event.poll:
            await client.send_poll(
                DEST_CH,
                question=event.poll.poll.question,
                answers=[a.text for a in event.poll.poll.answers],
                is_quiz=True,
                correct_option_id=event.poll.poll.correct_option_id,
                close_date=int(asyncio.get_event_loop().time()) + 60
            )

    await client.run_until_disconnected()

asyncio.run(main())
