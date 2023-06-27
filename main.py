import asyncio


from DiscordAPI import DiscordAPI
from TelegramAPI import TelegramAPI
from secrets import *

discord_api = DiscordAPI(telegram_instance=None)
telegram_api = TelegramAPI(discord_instance=discord_api)

# Set the TelegramAPI instance in the DiscordAPI instance
discord_api.telegram_instance = telegram_api


async def start_bot():
    # Start the Discord client
    discord_task = asyncio.create_task(discord_api.start())

    # Start the Telegram client
    telegram_task = asyncio.create_task(telegram_api.client.run_until_disconnected())

    # Wait for both tasks to complete
    await asyncio.gather(discord_task, telegram_task)

    # while True:
    #     await asyncio.sleep(3600)


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
