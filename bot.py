import telebot
import json

from os.path import exists

DATA_PATH = 'data.json'

with open('config.json') as file:
	config = json.load(file)

bot = telebot.TeleBot(config['BOT_TOKEN'])

ACTIVATED = False
CHAT_ID = ''

@bot.message_handler(commands=['start'])
def start(message):
	global CHAT_ID
	
	if CHAT_ID == '':
		bot.reply_to(message, "Bot activated")
		CHAT_ID = message.chat.id
		with open(DATA_PATH, 'w') as f:
			json.dump({'CHAT_ID': CHAT_ID}, f)

if __name__ == '__main__':
	bot.infinity_polling()