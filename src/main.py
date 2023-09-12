from typing import Any
import discord
from configparser import ConfigParser
import os

from datetime import datetime, date

# Config File
CONFIG = ConfigParser()
CONFIG.read("config.ini")

# Setting for data input (which kind of data bot can receive)
INTENTS = discord.Intents.default()
INTENTS.message_content = True

# Whitelist for Channels & Users
CHANNELS = ["test"]
USERS = ["_afo_", "a_foBOT#6965", "test_a_foBOT#8471"]

# Logs settings
LOGS_FOLDER = "logs"
ERROR_LOGS = "error_logs.txt"
USER_COMMAND_LOGS = "user_command_logs.txt"
D_MESSAGES_LOGS = "deleted_messages_logs.txt"

# Time
time_now = datetime.now()
CURRENT_TIME = time_now.strftime("%H:%M:%S")
date_today = date.today()
TODAY_DATE = date_today.strftime("%d-%m-%y")

# Bad Words Filter
PROHIBITED_WORDS = ["test word"]

# Secret Menu
SETTINGS_MENU = [
    False,  # 0 - Filtering
]


# Client Class
class MyClient(discord.Client):
    # On ready welcome message
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    # On Message Action
    async def on_message(self, message):
        # System console print
        print(f"Message from {message.author}: {message.content}")

        # Message filter
        try:
            if SETTINGS_MENU[0]:
                for word in PROHIBITED_WORDS:
                    if message.content.lower().count(word) > 0:
                        print("Offensive word - message deleted")
                        os.makedirs(LOGS_FOLDER, exist_ok=True)
                        log_file_path = os.path.join(LOGS_FOLDER, D_MESSAGES_LOGS)
                        with open(log_file_path, "a") as f:
                            f.write(
                                f"{TODAY_DATE} {CURRENT_TIME} | "
                                + f"User: {message.author}\nMessage: {message.content}\n"
                                + "-" * 20
                                + "\n"
                            )

                        print(f"User: {message.author} Message: {message.content}")
                        await message.channel.purge(limit=1)
                        break
        except Exception as error_message:
            # Send warning
            await message.channel.send("Something went wrong...")
            # Create folder if not exist
            os.makedirs(LOGS_FOLDER, exist_ok=True)
            # Append the error message to the 'logs.txt' file
            log_file_path = os.path.join(LOGS_FOLDER, ERROR_LOGS)
            with open(log_file_path, "a") as f:
                f.write(f"{TODAY_DATE} {CURRENT_TIME} | " + str(error_message) + "\n")

        # Message commands
        try:
            if str(message.channel) in CHANNELS and str(message.author) in USERS:
                # Secret Menu Call
                msg = message.content.replace("|", "")
                print(msg)
                if msg.count(CONFIG["secret_phrase"]["key"]) > 0:
                    # 0 - Secret Number / 1 - ID of option / 2 - Option Mode [0 - ON / 1 - Off]
                    splitted_message = [int(element) for element in msg.split()]
                    if len(splitted_message) == 3:
                        await message.channel.purge(limit=1)
                        SETTINGS_MENU[splitted_message[1]] = bool(splitted_message[2])
                        await message.channel.purge(limit=1)
                        await message.channel.send("Settings updated...")
                        embeded_element = discord.Embed(
                            title="Settings", description="Bot current settings"
                        )
                        embeded_element.add_field(
                            name="[0] Message Filter", value=str(SETTINGS_MENU[0])
                        )
                        await message.channel.send(content=None, embed=embeded_element)
                    else:
                        await message.channel.purge(limit=1)
                        embeded_element = discord.Embed(
                            title="Settings", description="Bot current settings"
                        )
                        embeded_element.add_field(
                            name="[0] Message Filter", value=str(SETTINGS_MENU[0])
                        )
                        await message.channel.send(content=None, embed=embeded_element)

                # Help Message [embedded]
                if message.content == "!help":
                    embeded_element = discord.Embed(
                        title="Help on a_foBOT",
                        description="Available commands",
                    )
                    embeded_element.add_field(
                        name="!help",
                        value="Displaying commands description",
                    )
                    embeded_element.add_field(
                        name="!user_count",
                        value="Displaying total number of users",
                    )
                    await message.channel.send(content=None, embed=embeded_element)

                # Counting on server users
                if message.content == "!user_count":
                    # Getting server id
                    id_ = client.get_guild(int(CONFIG["id"]["server_7sins"]))
                    await message.channel.send(f"Number of users: {id_._member_count}")

            # Saving logs if unauthorized user is going to push command
            else:
                os.makedirs(LOGS_FOLDER, exist_ok=True)
                log_file_path = os.path.join(LOGS_FOLDER, USER_COMMAND_LOGS)
                with open(log_file_path, "a") as f:
                    f.write(
                        f"{CURRENT_TIME} | "
                        + f"User: {message.author} tried to push command: {message.content}"
                        + "\n"
                    )
                print(
                    f"User: {message.author} tried to push command: {message.content}"
                )

        except Exception as error_message:
            # Send warning
            await message.channel.send("Something went wrong...")
            # Create folder if not exist
            os.makedirs(LOGS_FOLDER, exist_ok=True)
            # Append the error message to the 'logs.txt' file
            log_file_path = os.path.join(LOGS_FOLDER, ERROR_LOGS)
            with open(log_file_path, "a") as f:
                f.write(f"{TODAY_DATE} {CURRENT_TIME} | " + str(error_message) + "\n")


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
            f.write(f"{TODAY_DATE} {CURRENT_TIME} | " + str(error_message) + "\n")
