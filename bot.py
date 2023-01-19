import json
import sys
import base64
from loguru import logger
from telegram.ext import Updater, MessageHandler, Filters
from downloader import download_youtube_video
from utils import is_string_an_url, update_black_list, update_white_list, update_downloads_log
from clouds import mega_initialize_empty_drive
from time import sleep
from mega import Mega
from datetime import datetime


class Bot:
    def __init__(self, token):
        # create frontend object to the bot programmer
        self.updater = Updater(token, request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000}, use_context=True)
        # add _message_handler as main internal msg handler
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self._message_handler))

    def start(self):
        """Start polling msgs from users, this function never returns"""
        self.updater.start_polling()
        logger.info(f'Initializing mega drive'.format())
        mega_initialize_empty_drive(m)
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....'.format())
        self.updater.idle()

    def _message_handler(self, update, context):
        """Main messages handler"""
        self.send_text(update, f'Your original message: "{update.message.text}"')

    def send_text(self, update, text, chat_id=None, quote=False):
        """Sends text to a chat"""
        if chat_id:
            self.updater.bot.send_message(chat_id, text=text)
        else:
            # retry https://github.com/python-telegram-bot/python-telegram-bot/issues/1124
            update.message.reply_text(text, quote=quote)

    def send_audio(self, update, context, file_path):
        """Sends video to a chat"""
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(file_path, 'rb'))


class AVDownloader(Bot):
    def __init__(self, token):
        super().__init__(token)

    # Handle incoming messages
    def _message_handler(self, update, context):
        if update.message:
            chat_id = str(update.effective_message.chat_id)
            inbound_text = update.message.text
            if use_whitelist is True:
                if chat_id in whitelist:
                    logger.info(f'chat_id: "{chat_id}" is on whitelist'.format())
                    msg_handler_content(self, update, chat_id, inbound_text)
                else:
                    self.send_text(update, f'You are not allowed to use this bot')
                    logger.warning(f'chat_id: "{chat_id}" not allowed, skipping'.format())
                    logger.warning(f'message: "{inbound_text}"'.format())
            elif use_blacklist is True:
                if chat_id not in blacklist:
                    logger.info(f'chat_id: "{chat_id}" is not on blacklist'.format())
                    msg_handler_content(self, update, chat_id, inbound_text)
                else:
                    self.send_text(update, f'You are not allowed to use this bot.')
                    logger.warning(f'chat_id: "{chat_id}" not allowed, skipping'.format())
                    logger.warning(f'message: "{inbound_text}"'.format())
            else:
                msg_handler_content(self, update, chat_id, inbound_text)


def msg_handler_content(self, update, chat_id, inbound_text):
    dt_now = datetime.now()
    # Handle "/start" mode
    if update.message.text.lower() == '/start':
        fname = update.message.from_user.first_name
        lname = update.message.from_user.last_name
        username = update.message.from_user.username
        logger.info(f'chat_id: "{chat_id}"("{username}") - "{fname}" "{lname}" has started conversation'.format())
        self.send_text(update, f'Hello there, Welcome to AV Downloader.')
        sleep(1)
        self.send_text(update, f'Send a video link, get back download link for video/audio based on your input\n/help - Display help information.')
    # Handle "/help" mode
    elif update.message.text.lower() == '/help':
        logger.info(f'chat_id: "{chat_id}" - command received: /help'.format())
        self.send_text(update, f'Hello there, Welcome to AV Downloader.')
        sleep(1)
        self.send_text(update,
                       f'Send a video link, get back download link for video/audio based on your input\n/help - Display help information.')
    # Handle dev "/blacklist" command
    elif update.message.text.lower().startswith('/blacklist') and use_blacklist is True:
        logger.info(f'chat_id: "{chat_id}" - command received: /blacklist'.format())
        if chat_id == dev_chat_id:
            temp_chat_id = inbound_text.split(" ", 1)[1]
            blacklist.append(temp_chat_id) if temp_chat_id in blacklist else blacklist
            update_black_list(blacklist)
            self.send_text(update, f'Blacklist adding: "{temp_chat_id}"')
            logger.info(f'Blacklist adding: "{temp_chat_id}"'.format())
        else:
            logger.warning(f'chat_id: "{chat_id}" - Not allowed to use admin commands'.format())
            self.send_text(update, f'You are not allowed to use admin commands')
    # Handle dev "/whitelist" command
    elif update.message.text.lower().startswith('/whitelist') and use_whitelist is True:
        logger.info(f'chat_id: "{chat_id}" - command received: /whitelist'.format())
        if chat_id == dev_chat_id:
            temp_chat_id = inbound_text.split(" ", 1)[1]
            whitelist.append(temp_chat_id) if temp_chat_id in whitelist else whitelist
            update_white_list(whitelist)
            self.send_text(update, f'Whitelist adding: "{temp_chat_id}"')
            logger.info(f'Whitelist adding: "{temp_chat_id}"'.format())
        else:
            logger.warning(f'chat_id: "{chat_id}" - Not allowed to use admin commands'.format())
            self.send_text(update, f'You are not allowed to use admin commands')
    # Handle "/video" or "/v" mode
    elif update.message.text.lower().startswith('/video') or update.message.text.lower().startswith('/v'):
        temp = inbound_text.split(" ", 1)[1]
        logger.info(f'chat_id: "{chat_id}" - command received: /video or /v with ""{temp}"'.format())
        self.send_text(update, f'Processing link')
        logger.info(f'"{temp}"'.format())
        if inbound_text != '/video' and is_string_an_url(temp):
            logger.info(f'Downloading with mode 1(video) "{temp}"'.format())
            temp_file = download_youtube_video(temp, 1, m)
            if temp_file.startswith('Error'):
                downloads_log.append(f'"{dt_now}" - "{chat_id}" - Video - "{temp}" - Failure')
                self.send_text(update, f'{temp_file}')
            else:
                downloads_log.append(f'"{dt_now}" - "{chat_id}" - Video - "{temp}" - Success')
                self.send_text(update, f'The following download link will be available for the next 12 hours:\n{temp_file}')
            update_downloads_log(downloads_log)
            logger.info(f'Processing of "{inbound_text}" has been completed'.format())
        else:
            self.send_text(update, f'Invalid URL, for more information, send /help')
            logger.error(f'Invalid URL received by chat_id: "{chat_id}"'.format())
    # Handle "free-text" / URL text mode.
    else:
        logger.info(f'chat_id: "{chat_id}" - received "{inbound_text}"'.format())
        self.send_text(update, f'Processing link')
        temp = inbound_text.replace(' ', '')
        if is_string_an_url(temp):
            logger.info(f'Downloading with mode 2(audio) "{temp}"'.format())
            temp_file = download_youtube_video(temp, 2, m)
            if temp_file.startswith('Error'):
                downloads_log.append(f'"{dt_now}" - "{chat_id}" - Audio - "{inbound_text}" - Failure')
                self.send_text(update, f'{temp_file}')
            else:
                downloads_log.append(f'"{dt_now}" - "{chat_id}" - Audio - "{inbound_text}" - Success')
                self.send_text(update, f'The following download link will be available for the next 12 hours:\n{temp_file}')
            update_downloads_log(downloads_log)

            logger.info(f'Processing of "{inbound_text}" has been completed'.format())
        else:
            self.send_text(update, f'Invalid URL, for more information, send /help')
            logger.error(f'Invalid URL received by chat_id: "{chat_id}"'.format())


if __name__ == '__main__':
    # Execution check
    if sys.version_info < (3, 10):
        raise Exception("Must be using Python 3.10 and above")
    # Initialize Configurations
    logger.add("App_Log_{time}.log", rotation="30 days", backtrace=True, enqueue=False, catch=True)
    with open('config/secret.json') as json_handler:
        secret_data = json.load(json_handler)
    base64_bytes = secret_data["Telegram_Token"].encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    _token = message_bytes.decode()
    dev_chat_id = secret_data["Dev_Telegram_chat_id"]
    use_blacklist = secret_data["Use_Black_List"]
    use_whitelist = secret_data["Use_White_List"]
    # Initialize Mega connection
    base64_bytes = secret_data["Mega_User"].encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    email = message_bytes.decode()
    base64_bytes = secret_data["Mega_Pass"].encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    password = message_bytes.decode()
    mega = Mega()
    m = mega.login(email, password)
    # Initialize Whitelist
    whitelist = []
    if use_whitelist is True:
        with open('config/whitelist.txt', 'r') as whitelist_handler:
            for line in whitelist_handler:
                # remove linebreak which is the last character of the string
                chatid = line[:-1]
                # add item to the list
                whitelist.append(chatid)
        whitelist_handler.close()
    # Initialize Blacklist
    if use_blacklist is True:
        blacklist = []
        with open('config/blacklist.txt', 'r') as blacklist_handler:
            for line in blacklist_handler:
                # remove linebreak which is the last character of the string
                chatid = line[:-1]
                # add item to the list
                blacklist.append(chatid)
        blacklist_handler.close()
    # Initialize Downloads log
    downloads_log = []
    with open('config/downloads_log.txt', 'r') as downloads_log_handler:
        for line in downloads_log_handler:
            # remove linebreak which is the last character of the string
            logline = line[:-1]
            # add item to the list
            downloads_log.append(logline)
    downloads_log_handler.close()

    my_bot = AVDownloader(_token)
    my_bot.start()
