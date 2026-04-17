import asyncio
from telethon import TelegramClient, events

API_ID = 35089639
API_HASH = '0c46a9a35e7db749b8a9b87b0bdb0aec'

SOURCE_CH = 'ssc_crack_gk'
DEST_CH = 'toforwerd'

# 🔥 नया session file name
client = TelegramClient('render_session', API_ID, API_HASH)

async def main():
    await client.start()
    print("✅ Logged in using render_session.session")

    # Old polls
    async for msg in client.iter_messages(SOURCE_CH, limit=50):
        if msg.poll:
            p = msg.poll.poll if hasattr(msg.poll, 'poll') else msg.poll
            await client.send_poll(
                DEST_CH,
                question=p.question,
                answers=[a.text for a in p.answers],
                is_quiz=True,
                correct_option_id=getattr(p, 'correct_option_id', None),
                close_date=int(asyncio.get_event_loop().time()) + 60
            )
            print(f"✅ Recreated {msg.id}")
            await asyncio.sleep(2)

    @client.on(events.NewMessage(chats=SOURCE_CH))
    async def handler(e):
        if e.message.poll:
            p = e.message.poll.poll if hasattr(e.message.poll, 'poll') else e.message.poll
            await client.send_poll(
                DEST_CH,
                question=p.question,
                answers=[a.text for a in p.answers],
                is_quiz=True,
                correct_option_id=getattr(p, 'correct_option_id', None),
                close_date=int(asyncio.get_event_loop().time()) + 60
            )
            print(f"✅ New poll recreated")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
