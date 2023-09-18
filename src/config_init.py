import configparser
import os

config = configparser.ConfigParser()

discord_bot_token = os.getenv("DISCORD_TOKEN")
key = os.getenv("MENU_KEY")

config["discord"] = {"token": str(discord_bot_token)}
config["secret_phrase"] = {"key": str(key)}

with open("config.ini", "w") as configfile:
    config.write(configfile)
