import json
from loguru import logger
from datetime import datetime, timedelta


# Mega Code:
def mega_initialize_empty_drive(m):
    try:
        logger.info(f'Attempting to initialize drive'.format())
        # get account files
        files = m.get_files()
        # iterate over files
        for file in files:
            if file != 'iEolQT4L' and file != 'GJ5hBTiL' and file != 'uEhxhJxa':
                logger.info(f'Deleting file from drive, ID: "{file}"'.format())
                m.destroy(file)
        logger.info(f'initialize complete'.format())
    except Exception as e:
        logger.error(e)


def mega_check_if_exists(filename, m):
    try:
        logger.info(f'Checking if file with "{filename}" exists already'.format())
        file = m.find(filename, exclude_deleted=True)
        if file:
            link = m.get_link(file)
            logger.info(f'check complete: "{filename}" exists, resetting lifespan and returning link:\n{link}'.format())
            return link
        else:
            logger.info(f'File does not exist in mega drive.'.format())
            return 'Error: File does not exist'
    except Exception as e:
        logger.error(e)
        return 'Error: An error has occurred, please check logs'


def mega_upload_share_file(filename, m):
    try:
        logger.info(f'Attempting to Upload and Share: {filename}'.format())
        file = m.upload(filename)
        link = m.get_upload_link(file)
        logger.info(f'Uploaded: {filename}\nShare link: {link}'.format())
        return link
    except Exception as e:
        logger.error(e)
        return 'Error: An error has occurred, please check logs'


def manage_downloads(filename, m):
    try:
        # Mega section
        logger.info(f'File does not exist in mega drive: "{filename}", Attempting to upload and share'.format())
        link = mega_upload_share_file(filename, m)
        dt_now = datetime.now()
        dt_future = dt_now + timedelta(hours=12)
        logger.info(f'Attempting to update downloads.json file with key: "{filename}" and value: "{dt_future}"'.format())
        # Local file section
        with open('config/downloads.json') as json_list:
            downloads = json.load(json_list)
        json_list.close()
        downloads[filename] = f'{dt_future}'
        # update local downloads.json file
        with open('config/downloads.json', 'w') as json_list_w:
            json.dump(downloads, json_list_w, indent=4)
        json_list_w.close()
        logger.info(f"downloads.json update success.".format())
        # Return link after success on everything
        return link
    except Exception as e:
        logger.error(e)
        return 'Error: An error has occurred, please check logs'

# TODO
# implement AWS S3 code
