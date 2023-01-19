# AV-Downloader-Telegram-Bot

### Features
- Supports downloading of videos from links and converting to h265 video format.
- Supports downloading of videos from links and converting to mp3 format.
- Supports Uploading content to Mega drive and share download links.
- Supports Hebrew/English/Russian/Arabic languages in files names.
- Supports Whitelist / Blacklist features

### TBD:
- AWS S3 support.
- Local file sending support.
- Auto delete from Mega drive expired downloads files.

### Installation:

- [ ] Use Python 3.10 or above.
- [ ] Create Telegram bot and save the Token for it.
- [ ] Remove "-example" from files under config folder.
- [ ] Remove placeholder content from .txt files under config folder(<PLACE HOLDER>). 
- [ ] Install FFMPEG.
- [ ] Install relevant packages from requirements.txt file:
`$ pip install -r requirements.txt`
- [ ] Configure the secret.json file:

| Key                   | Value                                                      |
| ---------             |------------------------------------------------------------|
| Dev_Telegram_chat_id  | (String)Telegram Chat ID of the Admin/Developer of the bot |
| version               | (String)1.0                                                |
| Telegram_Token        | (String)Token for the Telegram Bot - BASE64 Encoded        |
| Telegram_Username     | (String)Username of the Telegram Bot                       |
| Telegram_Name         | (String)Name of the Telegram Bot                           |
| Telegram_Link         | (String)Link to the Telegram Bot                           |
| Mega_Full_Name        | (String)Name of the Telegram Bot                           |
| Mega_User             | (String)Username for MEGA drive - BASE64 Encoded           |
| Mega_Pass             | (String)Password for MEGA drive - BASE64 Encoded           |
| Use_Black_List        | (Boolean)True/False - Cannot be used with Whitelist        |
| Use_White_List        | (Boolean)True/False - Cannot be used with Blacklist        |