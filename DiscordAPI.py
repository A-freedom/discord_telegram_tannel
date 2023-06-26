from os import makedirs,path
import discord

from constance import *
from tools import download_file, move_files_up_and_remove_folder


class DiscordAPI:
    def __init__(self, telegram_instance):
        self.telegram_instance = telegram_instance
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_message(message):
            # TODO find a better way to to do this .
            if message.channel.id == disocrd_channel_id_int:
                # Check if the message is from a user (not a bot)
                if not message.author.bot:
                    download_file_path = None
                    file_path = None
                    if message.attachments:
                        for attachment in message.attachments:
                            author_id = message.author.id
                            message_id = message.id

                            url = attachment.url
                            filename = attachment.filename
                            file_path = f'media\\discord\\{author_id}\\temp{message_id}'
                            download_file_path = path.join(file_path, filename)
                            makedirs(file_path, exist_ok=True)
                            download_file(url, filename, file_path)
                            print('ok')

                    content = message.content
                    display_name = message.author.display_name
                    response = display_name + '\n' + content

                    if download_file_path is not None:
                        with open(download_file_path, 'rb') as file:
                            await message.channel.send(response, file=discord.File(file))
                            file.close()
                            move_files_up_and_remove_folder(file_path)

                    else:
                        await message.channel.send(response)

        @self.client.event
        async def on_error(event, *args, **kwargs):
            import traceback
            traceback.print_exc()

    async def send_message(self, content, file_paths=None):
        channel = self.client.get_channel(disocrd_channel_id_int)
        if channel:
            await channel.send(content)
            if file_paths is None:
                return
            for file_path in file_paths:
                # Create a discord.File object from the file path
                file = discord.File(file_path)
                # Send the file as an attachment in the channel
                await channel.send(file=file)

    async def start(self):
        await self.client.start(discord_token_str)
