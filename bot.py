import asyncio
import time
import os
from telethon import TelegramClient, events

# -------------------------------
API_ID = 35089639
API_HASH = '0c46a9a35e7db749b8a9b87b0bdb0aec'
PHONE = '+917599181164'
PASSWORD = '181164'

SOURCE_CHANNELS = ['ssc_crack_gk']
DEST_CHANNEL = 'toforwerd'
# -------------------------------

PROCESSED_FILE = 'processed.txt'

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE) as f:
            return set(line.strip() for line in f)
    return set()

def save_processed(poll_id):
    with open(PROCESSED_FILE, 'a') as f:
        f.write(f"{poll_id}\n")

async def recreate_poll(client, event, poll_id):
    # Poll data extract
    msg = event if hasattr(event, 'poll') else event.message
    if hasattr(msg.poll, 'poll'):
        poll = msg.poll.poll
    else:
        poll = msg.poll

    options = [ans.text for ans in poll.answers]
    correct_id = poll.correct_option_id if hasattr(poll, 'correct_option_id') else None
    close_at = int(time.time()) + 60

    await client.send_poll(
        DEST_CHANNEL,
        question=poll.question,
        options=options,
        is_quiz=True,
        correct_option_id=correct_id,
        close_date=close_at,
        explanation="✅ Poll closed. Correct answer is shown above."
    )
    save_processed(str(poll_id))
    print(f"✅ Recreated poll {poll_id} with 1-min timer")

async def main():
    print("🤖 Starting Poll Forwarder...")
    client = TelegramClient('forwarder_session', API_ID, API_HASH)

    # Auto login
    await client.start(phone=PHONE, password=PASSWORD)
    print("✅ Logged into Telegram")

    # Scan old polls
    print("📜 Scanning old polls...")
    processed = load_processed()
    async for msg in client.iter_messages(SOURCE_CHANNELS[0], limit=100):
        if msg.poll and str(msg.id) not in processed:
            await recreate_poll(client, msg, msg.id)
            await asyncio.sleep(2)

    # Listen to new polls
    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def new_poll_handler(event):
        if event.message.poll and str(event.message.id) not in load_processed():
            await recreate_poll(client, event.message, event.message.id)

    print("⏳ Watching for new polls... (Ctrl+C to stop)")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
