from os import path, makedirs
import discord
from secrets import *
from tools import download_file, move_files_up_and_remove_folder


class DiscordAPI:
    def __init__(self, telegram_instance):
        self.telegram_instance = telegram_instance
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_message(message):
            author_id = message.author.id
            message_id = message.id

            if message.channel.id == disocrd_channel_id_int and not message.author.bot:
                download_file_paths = []
                file_path = f'media/discord/{author_id}/temp{message_id}'
                makedirs(file_path, exist_ok=True)

                if message.attachments:
                    for attachment in message.attachments:
                        url = attachment.url
                        filename = attachment.filename
                        download_file_paths.append(path.join(file_path, filename))
                        download_file(url, filename, file_path)

                content = message.content
                display_name = message.author.display_name
                response = f'#{display_name} :: {content}'

                await self.telegram_instance.send_message_to_channel(response, download_file_paths)
                move_files_up_and_remove_folder(file_path)

        @self.client.event
        async def on_error(event, *args, **kwargs):
            import traceback
            traceback.print_exc()

    async def send_message(self, content, file_paths=None):
        channel = self.client.get_channel(disocrd_channel_id_int)
        if channel:
            await channel.send(content)
            if file_paths:
                for file_path in file_paths:
                    file = discord.File(file_path)
                    await channel.send(file=file)

    async def start(self):
        await self.client.start(discord_token_str)
