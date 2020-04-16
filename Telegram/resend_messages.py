import time
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
from telethon import errors


def main():
    api_id = "XXXXX"
    api_hash = "XXXXX"
    phone = '+4XXXXX'
    done_path = r"XXXXX\done.txt"
    session_file_path = r"XXXXX\XXXXX.session"
    channel_id = XXXXX
    users = ['XXXXX', 'me']

    try:
        # Load sended ids
        with open(done_path) as f:
            done = [int(row.replace("\n", "")) for row in f.readlines()]
    except FileNotFoundError:
        done = list()

    # Connect to telegram client
    client = TelegramClient(session_file_path, api_id, api_hash)
    client.connect()

    # If client not autenticated, request SMS code
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    try:
        # Load messages
        messages = client.get_messages(PeerChannel(channel_id), 10)
        for message in messages:
            # Check if message was sended
            if message.id not in done:
                # Save new message id
                with open(done_path, "a") as f:
                    f.write("{}\n".format(message.id))
                # Send message to all users
                for user in users:
                    client.send_message(user, message.text)
                    time.sleep(1)
    except errors.FloodWaitError as e:
        print('Have to sleep', e.seconds, 'seconds')
        time.sleep(e.seconds)


if __name__ == '__main__':
    main()
