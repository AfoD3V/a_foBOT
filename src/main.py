from typing import Any
import discord
import os
from discord.flags import Intents
from settings import *


class MyClient(discord.Client):
    """
    MyClient class allowing us to run an instance of discord bot, this bot has few methods
    with no return in most cases.

    Methods
    -------
    `on_ready()`
        This method is to print initial message when bot is going online.

    `on_message()`
        This method allowing us to read user messages,
        and make proper interactions accordingly to the message.

    `message_filter()`
        This method allowing us to filter user messages,
        if user message is consist of any of the prohibited words that are stored in
        "settings.py" -> "PROHIBITED_WORDS" variable, than it is going to be deleted.

    `secret_menu_command()`
        This method allowing us to call secret menu, which is storing all the options
        that are possible to interact with from user level. We can call that menu by specifying
        secret key that is stored in "config.ini" -> "["secret_phrase"]["key"]".
        To call menu and interact with it we need to go like that -> `123456789 0 1` or `||123456789 0 1||`
        - Where:
        - [0] -> "123456789" -> secret key
        - [1] -> "0"         -> option to select
        - [2] -> "1"         -> option value {0 False / 1 True}

    `help_command()`
        This method allowing us to call embedded hint menu with all available commands.
    """

    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.SETTINGS_MENU = SETTINGS_MENU

    async def message_filter(self, message: str) -> None:
        """Filter user message, if user message is consist of prohibited words,
        and filter option is set to TRUE - delete user message

        Input:
         - message:     actual message received from the discord server side"""
        try:
            if self.SETTINGS_MENU[0]:
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

    async def secret_menu_command(self, message: str, msg: str) -> None:
        """Call secret menu if message is equal to -> secret_key or ||secret_key||

        Input:
         - message: actual message received from the discord server side"""
        if msg.count(os.environ["SECRET_KEY"]) > 0:
            # 0 - Secret Number / 1 - ID of option / 2 - Option Mode [0 - ON / 1 - Off]
            splitted_message = [int(element) for element in msg.split()]
            if len(splitted_message) == 3:
                await message.channel.purge(limit=1)
                self.SETTINGS_MENU[splitted_message[1]] = bool(splitted_message[2])
                await message.channel.purge(limit=1)
                await message.channel.send("Settings updated...")
                embeded_element = discord.Embed(
                    title="Settings", description="Bot current settings"
                )
                embeded_element.add_field(
                    name="[0] Message Filter", value=str(self.SETTINGS_MENU[0])
                )
                await message.channel.send(content=None, embed=embeded_element)
            else:
                await message.channel.purge(limit=1)
                embeded_element = discord.Embed(
                    title="Settings", description="Bot current settings"
                )
                embeded_element.add_field(
                    name="[0] Message Filter", value=str(self.SETTINGS_MENU[0])
                )
                await message.channel.send(content=None, embed=embeded_element)

    async def help_command(self, message):
        """Call embedded hint menu, which is providing clues for available commands

        Input:
         - message: actual message received from the discord server side"""

        if message.content == "!help":
            embeded_element = discord.Embed(
                title="Help on a_foBOT",
                description="Available commands",
            )
            embeded_element.add_field(
                name="!help",
                value="Displaying commands description",
            )
            await message.channel.send(content=None, embed=embeded_element)

    async def on_ready(self):
        """Print initial message when ready"""
        print(f"Logged on as {self.user}")

    # On Message Action
    async def on_message(self, message):
        """This method is interacting with messages typed by users on the server side,
        if any message is going to match command than proper method is going to get executed

        Input:
         - message: actual message received from the discord server side
        """
        # System console print
        print(f"Message from {message.author}: {message.content}")

        # Message Filtering
        await self.message_filter(message)

        # On message actions
        try:
            if str(message.channel) in CHANNELS and str(message.author) in USERS:
                # Secret Menu Call
                msg = message.content.replace("|", "")
                await self.secret_menu_command(message, msg)

                # Help Message [embedded]
                await self.help_command(message)

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
        client.run(os.environ["DISCORD_TOKEN"])
    # If anny error occure - save logs
    except Exception as error_message:
        # Create folder if not exist
        os.makedirs(LOGS_FOLDER, exist_ok=True)
        # Append the error message to the 'logs.txt' file
        log_file_path = os.path.join(LOGS_FOLDER, ERROR_LOGS)
        with open(log_file_path, "a") as f:
            f.write(f"{TODAY_DATE} {CURRENT_TIME} | " + str(error_message) + "\n")
