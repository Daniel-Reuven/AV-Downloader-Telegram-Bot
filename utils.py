import validators
from validators import ValidationFailure


def is_string_an_url(url_string: str) -> bool:
    result = validators.url(url_string)
    if isinstance(result, ValidationFailure):
        return False
    return result


def update_white_list(chat_ids):
    with open('config/whitelist.txt', 'w') as filehandler:
        for chatid in chat_ids:
            filehandler.write('%s\n' % chatid)
    filehandler.close()


def update_black_list(banned_list):
    with open('config/blacklist.txt', 'w') as filehandler:
        for chatid in banned_list:
            filehandler.write('%s\n' % chatid)
    filehandler.close()


def update_downloads_log(downloads_log):
    with open('config/downloads_log.txt', 'w') as filehandler:
        for item in downloads_log:
            filehandler.write('%s\n' % item)
    filehandler.close()
