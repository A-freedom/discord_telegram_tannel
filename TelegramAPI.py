from os import makedirs

from telethon import TelegramClient, events

# from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from constance import *
from tools import get_file_paths, move_files_up_and_remove_folder


class TelegramAPI:
    def __init__(self, discord_instance):
        self.discord_instance = discord_instance
        self.client = TelegramClient('session_name', telegram_api_id_str, telegram_api_hash_str)
        self.client.start()

        @self.client.on(events.NewMessage(chats=telegram_channel_str))
        async def handler(event):
            user_id = event.message.chat_id
            message_id = event.message.id
            temp_name = f'temp{message_id}'
            # TODO the next line is form test only make sure to remove it after you finish
            await event.reply('pong!')

            # if event.message.media:
            #     # Check the type of media
            #     if isinstance(event.message.media, MessageMediaPhoto):
            #         print("The message has a photo.")
            #     elif isinstance(event.message.media, MessageMediaDocument):
            #         print("The message has a document.")
            #     else:
            #         print("The message has media, but the type is unknown.")
            # else:
            #     print("The message does not have any media.")

            file_path = None
            if event.message.media:
                file_path = f'media\\telegram\\{user_id}\\{temp_name}'
                makedirs(file_path, exist_ok=True)
                await event.message.download_media(file_path)
            event.message.text = event.message.post_author + event.message.text

            files_paths = get_file_paths(file_path) if file_path is not None else []
            await self.discord_instance.send_message(event.message.text, files_paths)
            move_files_up_and_remove_folder(file_path)
