from typing import Any
import discord
from configparser import ConfigParser
import os
from discord.flags import Intents
from datetime import datetime

# Config File
CONFIG = ConfigParser()
CONFIG.read("config.ini")

# Setting for data input (which kind of data bot can receive)
INTENTS = discord.Intents.default()
INTENTS.message_content = True

# Whitelist for Channels & Users
CHANNELS = ["test"]
USERS = ["_afo"]

# Logs settings
LOGS_FOLDER = "logs"
ERROR_LOGS = "error_logs.txt"
USER_COMMAND_LOGS = "user_command_logs.txt"

# Time
time_now = datetime.now()
CURRENT_TIME = time_now.strftime("%H:%M:%S")


# Client Class
class MyClient(discord.Client):
    # On ready welcome message
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    # On Message Action
    async def on_message(self, message):
        # System console print
        print(f"Message from {message.author}: {message.content}")

        # Message commands
        if str(message.channel) in CHANNELS and str(message.author) in USERS:
            # Test message
            if message.content == "!test":
                await message.channel.send("test")
            # Counting on server users
            if message.content == "!user_count":
                id_ = client.get_guild(int(CONFIG["id"]["server_7sins"]))
                await message.channel.send(f"Number of users: {id_._member_count}")
        else:
            os.makedirs(LOGS_FOLDER, exist_ok=True)
            log_file_path = os.path.join(LOGS_FOLDER, USER_COMMAND_LOGS)
            with open(log_file_path, "a") as f:
                f.write(
                    f"{CURRENT_TIME} | "
                    + f"User: {message.author} tried to push command: {message.content}"
                    + "\n"
                )
            print(f"User: {message.author} tried to push command: {message.content}")


if __name__ == "__main__":
    # Setup for Client
    client = MyClient(intents=INTENTS)

    # Run Client
    try:
        client.run(CONFIG["discord"]["token"])

    # If anny error occure - save logs
    except Exception as error_message:
        # Create folder if not exist
        os.makedirs(LOGS_FOLDER, exist_ok=True)

        # Append the error message to the 'logs.txt' file
        log_file_path = os.path.join(LOGS_FOLDER, ERROR_LOGS)
        with open(log_file_path, "a") as f:
            f.write(f"{CURRENT_TIME} | " + str(error_message) + "\n")
