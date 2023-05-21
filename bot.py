import telebot
import json
from os.path import exists

DATA_PATH = 'data.json'

with open('config.json') as file:
	config = json.load(file)

bot = telebot.TeleBot(config['BOT_TOKEN'])

ENABLED = False
CHAT_ID = ''

@bot.message_handler(commands=['start'])
def start(message):
	global CHAT_ID
	
	if CHAT_ID == '':
		bot.reply_to(message, "Bot is now tied to this chat")
		CHAT_ID = message.chat.id
		with open(DATA_PATH, 'w') as f:
			data = {}
			data['CHAT_ID'] = CHAT_ID
			data['ENABLED'] = str(ENABLED)
			json.dump(data, f)
	elif CHAT_ID == message.chat.id:
		bot.reply_to(message, "Bot is already tied to this chat")
	else:
		bot.reply_to(message, "Bot is already tied to another chat")
		
def toggle_enabled(message, value: bool):
	global ENABLED
	ENABLED = value
	bot.reply_to(message, "Enabled" if value else "Disabled" )
	with open(DATA_PATH) as file:
		data = json.load(file)
		data['ENABLED'] = str(ENABLED)
		with open(DATA_PATH, 'w') as f:
			json.dump(data, f)
			
@bot.message_handler(commands=['enable'])
def enable(message):
	if message.chat.id != CHAT_ID:
		bot.reply_to(message, "You have no access to this bot.")
		return
	
	if not ENABLED:
		toggle_enabled(message, True)
	else:
		bot.reply_to(message, "Already enabled")
		
@bot.message_handler(commands=['disable'])
def disable(message):
	if message.chat.id != CHAT_ID:
		bot.reply_to(message, "You have no access to this bot.")
		return
	
	if ENABLED:
		toggle_enabled(message, False)
	else:
		bot.reply_to(message, "Already disabled")

if exists(DATA_PATH):
	with open(DATA_PATH) as file:
		data = json.load(file)
		CHAT_ID = data['CHAT_ID']
		data['ENABLED'] = 'False'
		with open(DATA_PATH, 'w') as f:
			json.dump(data, f)

if __name__ == '__main__':
	bot.infinity_polling()