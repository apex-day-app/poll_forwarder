from telethon import TelegramClient, events
import asyncio
import time
import os

API_ID = 35089639
API_HASH = '0c46a9a35e7db749b8a9b87b0bdb0aec'
SOURCE_CHANNELS = ['ssc_crack_gk']
DEST_CHANNEL = 'toforwerd'

client = TelegramClient('forwarder', API_ID, API_HASH)
processed = set()
file = 'processed.txt'

if os.path.exists(file):
    with open(file, 'r') as f:
        processed = set(line.strip() for line in f)

async def recreate_poll(event, poll_id):
    if hasattr(event.poll, 'poll'):
        poll = event.poll.poll
    else:
        poll = event.poll
    
    options = [a.text for a in poll.answers]
    correct = poll.correct_option_id if hasattr(poll, 'correct_option_id') else None
    close_in = int(time.time()) + 60
    
    try:
        await client.send_poll(
            DEST_CHANNEL,
            question=poll.question,
            options=options,
            is_quiz=True,
            correct_option_id=correct,
            close_date=close_in,
            explanation="✅ Poll closed! Correct answer is above."
        )
        print(f"✅ Recreated poll {poll_id} with 1 min timer")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    if event.message.poll and str(event.message.id) not in processed:
        if await recreate_poll(event.message, event.message.id):
            processed.add(str(event.message.id))
            with open(file, 'a') as f:
                f.write(f"{event.message.id}\n")

async def scan_old():
    print("\n📜 Scanning old polls...")
    async for msg in client.iter_messages(SOURCE_CHANNELS[0], limit=100):
        if msg.poll and str(msg.id) not in processed:
            await recreate_poll(msg, msg.id)
            processed.add(str(msg.id))
            with open(file, 'a') as f:
                f.write(f"{msg.id}\n")
            await asyncio.sleep(2)

async def main():
    await client.start()
    print("=" * 50)
    print("🤖 POLL FORWARDER (RENDER VERSION)")
    print(f"📡 From: {SOURCE_CHANNELS}")
    print(f"🎯 To: {DEST_CHANNEL}")
    print("⏰ Each poll will close in 1 minute with answer")
    print("=" * 50)
    await scan_old()
    print("⚡ Waiting for new polls...\n")
    await client.run_until_disconnected()

asyncio.run(main())
