import discord

import secrets

# Your Discord API token
TOKEN = secrets.discord_token_str

# The ID of the channel you want to retrieve the latest message from
channel_id = secrets.disocrd_channel_id_int

# Create a Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Fetch the channel object
    channel = client.get_channel(channel_id)

    # Fetch the latest message in the channel
    latest_message = await channel.fetch_message(channel.last_message_id)

    # Print the content of the latest message
    print(latest_message.content)


# Start the Discord client
client.run(TOKEN)
