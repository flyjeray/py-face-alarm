# how to run

rename config_example.json to config.json and paste your telegram bot token there

use run.bat script to open both scripts (just saves time).

if someone tries to use your pc when you are away, script will send their photo and lock your pc.

## tie to chat

after bot.py starts, run /start to activate bot and tie it to your chat.

It won't retie to another chat until script is restarted.

After running script, it will save your ChatID - you will not need to run /start again.

## control alarm

by default, alarm is disabled. run /enabled or /disabled commands in Telegram to control alarm.

It won't send images if disabled, but will still save last user in photo.png.
