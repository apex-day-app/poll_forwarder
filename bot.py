import asyncio
from telethon import TelegramClient, events
import time
import os

# ========================================
API_ID = 35089639
API_HASH = '0c46a9a35e7db749b8a9b87b0bdb0aec'
SOURCE_CHANNELS = ['ssc_crack_gk']
DEST_CHANNEL = 'toforwerd'
# ========================================

PROCESSED_FILE = 'processed.txt'

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_processed(poll_id):
    with open(PROCESSED_FILE, 'a') as f:
        f.write(f"{poll_id}\n")

async def main():
    print("=" * 55)
    print("🤖 POLL FORWARDER (Python 3.11)")
    print(f"📡 Source: {SOURCE_CHANNELS}")
    print(f"🎯 Destination: {DEST_CHANNEL}")
    print("=" * 55)
    
    client = TelegramClient('forwarder_session', API_ID, API_HASH)
    await client.start()
    print("✅ Connected to Telegram!\n")
    
    # पुराने पोल्स स्कैन करो
    print("📜 Scanning old polls...")
    processed = load_processed()
    count = 0
    
    async for msg in client.iter_messages(SOURCE_CHANNELS[0], limit=100):
        if msg.poll and str(msg.id) not in processed:
            if hasattr(msg.poll, 'poll'):
                poll = msg.poll.poll
            else:
                poll = msg.poll
            
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
                    explanation="✅ Poll closed! Answer above."
                )
                save_processed(str(msg.id))
                count += 1
                print(f"✅ Recreated poll {msg.id}")
            except Exception as e:
                print(f"❌ Error: {e}")
            await asyncio.sleep(2)
    
    print(f"✅ Processed {count} old polls\n")
    
    # नए पोल्स के लिए
    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        if event.message.poll:
            pid = str(event.message.id)
            if pid in load_processed():
                return
            
            if hasattr(event.message.poll, 'poll'):
                poll = event.message.poll.poll
            else:
                poll = event.message.poll
            
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
                    explanation="✅ Poll closed! Answer above."
                )
                save_processed(pid)
                print(f"✅ New poll recreated: {pid}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    print("⚡ Waiting for new polls...\n")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
