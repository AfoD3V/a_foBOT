import discord
from configparser import ConfigParser
import os

# Config File
CONFIG = ConfigParser()
CONFIG.read("config.ini")

# Setting for data input (which kind of data bot can receive)
INTENTS = discord.Intents.default()
INTENTS.message_content = True


# Client Class
class MyClient(discord.Client):
    # On ready welcome message
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


if __name__ == "__main__":
    # Setup for Client
    client = MyClient(intents=INTENTS)

    # Run Client
    try:
        client.run(CONFIG["discord"]["token"])

    # If anny error occure - save logs
    except Exception as error_message:
        # Settings for logs
        logs_folder = "logs"
        logs_file = "logs.txt"

        # Create folder if not exist
        os.makedirs(logs_folder, exist_ok=True)

        # Append the error message to the 'logs.txt' file
        log_file_path = os.path.join(logs_folder, logs_file)
        with open(log_file_path, "a") as f:
            f.write(str(error_message) + "\n")
