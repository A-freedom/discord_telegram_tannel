from os import makedirs

from telethon import TelegramClient, events

from secrets import *
from tools import get_file_paths, move_files_up_and_remove_folder


class TelegramAPI:
    def __init__(self, discord_instance):
        self.discord_instance = discord_instance
        self.client = TelegramClient('session_name', telegram_api_id_str, telegram_api_hash_str)
        self.client.start()

        @self.client.on(events.NewMessage(chats=telegram_channel_int))
        async def handler(event):
            user_id = event.message.chat_id
            message_id = event.message.id
            temp_name = f'temp{message_id}'

            file_path = None
            if event.message.media:
                file_path = f'media/telegram/{user_id}/{temp_name}'
                makedirs(file_path, exist_ok=True)
                await event.message.download_media(file_path)
            event.message.text = event.message.post_author + event.message.text

            event.message.text = f'{event.message.post_author}\n--------------------\n{event.message.text}'
            files_paths = get_file_paths(file_path) if file_path is not None else []
            await self.discord_instance.send_message(event.message.text, files_paths)
            move_files_up_and_remove_folder(file_path)

    async def send_message_to_channel(self, caption, file_path):
        channel_entity = await self.client.get_entity(telegram_channel_int)
        if file_path is None:
            await self.client.send_file(channel_entity, caption=caption)
        await self.client.send_file(channel_entity, file=file_path, caption=caption)
