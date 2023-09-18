from datetime import datetime, date
from configparser import ConfigParser
import discord

"""Secret Menu"""
SETTINGS_MENU = [
    False,  # 0 - Filtering
]


"""Bad Words Filter"""
PROHIBITED_WORDS = ["test word"]


"""Time"""
time_now = datetime.now()
CURRENT_TIME = time_now.strftime("%H:%M:%S")
date_today = date.today()
TODAY_DATE = date_today.strftime("%d-%m-%y")


"""Logs Settings"""
LOGS_FOLDER = "logs"
ERROR_LOGS = "error_logs.txt"
USER_COMMAND_LOGS = "user_command_logs.txt"
D_MESSAGES_LOGS = "deleted_messages_logs.txt"


"""Whitelist for Channels & Users"""
CHANNELS = ["test"]
USERS = ["_afo_", "a_foBOT#6965", "test_a_foBOT#8471"]


"""Config File"""
CONFIG = ConfigParser()
CONFIG.read("config.ini")


"""Setting for data input (which kind of data bot can receive)"""
INTENTS = discord.Intents.default()
INTENTS.message_content = True
