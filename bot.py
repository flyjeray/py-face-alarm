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
	else:
		bot.reply_to(message, "Bot is already tied to another chat")
			
@bot.message_handler(commands=['enable'])
def enable(message):
	global ENABLED
	
	if message.chat.id != CHAT_ID:
		bot.reply_to(message, "You have no access to this bot.")
		return
	
	if not ENABLED:
		ENABLED = True
		bot.reply_to(message, "Enabled")
		with open(DATA_PATH) as file:
			data = json.load(file)
			data['ENABLED'] = str(ENABLED)
			with open(DATA_PATH, 'w') as f:
				json.dump(data, f)
	else:
		bot.reply_to(message, "Already enabled")
		
@bot.message_handler(commands=['disable'])
def disable(message):
	global ENABLED
	
	if message.chat.id != CHAT_ID:
		bot.reply_to(message, "You have no access to this bot.")
		return
	
	if ENABLED:
		ENABLED = False
		bot.reply_to(message, "Disabled")
		with open(DATA_PATH) as file:
			data = json.load(file)
			data['ENABLED'] = str(ENABLED)
			with open(DATA_PATH, 'w') as f:
				json.dump(data, f)
	else:
		bot.reply_to(message, "Already disabled")


if exists(DATA_PATH):
	with open(DATA_PATH) as file:
		data = json.load(file)
		CHAT_ID = data['CHAT_ID']

if __name__ == '__main__':
	bot.infinity_polling()