## this file is based on version 13.7 of python telegram chatbot and version 1.26.18 of u
## chatbot.py
import telegram
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PrefixHandler)
# The messageHandler is used for all message updates
import configparser
import logging

import redis
from ChatGPT_HKBU import HKBU_ChatGPT
global redis1



def main():
	# Load your token and create an Updater for your Bot
	config = configparser.ConfigParser()
	config.read('config.ini')
	updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
	dispatcher = updater.dispatcher
	global redis1
	redis1 = redis.Redis(host=(config['REDIS']['HOST']),
		password=(config['REDIS']['PASSWORD']),
		port=(config['REDIS']['REDISPORT']))

	# You can set this logging module, so you will know when and why things do not work a
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)
	
	# register a dispatcher to handle message: here we register an echo dispatcher
	# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
	# dispatcher.add_handler(echo_handler)
	
	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("add", add))
	dispatcher.add_handler(CommandHandler("help", help_command))

	# lab_4_writeup_question_3, not work the command handler or prefix handler not work with " "
	# dispatcher.add_handler(CommandHandler("hello Kevin", hello_kevin))
	# dispatcher.add_handler(MessageHandler(Filters.text, hello_kevin))


	# dispatcher for chatgpt
	global chatgpt
	chatgpt = HKBU_ChatGPT(config)
	chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),equiped_chatgpt)
	dispatcher.add_handler(chatgpt_handler)

	

	# To start the bot:
	updater.start_polling()
	updater.idle()



def echo(update, context):
	reply_message = update.message.text.upper()
	logging.info("Update: " + str(update))
	logging.info("context: " + str(context))
	context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def help_command(update: Updater, context: CallbackContext) -> None:
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /add is issued."""
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0] # /add keyword <-- this should store the keyword
		redis1.incr(msg)

		update.message.reply_text('You have said ' + msg + ' for ' +
			redis1.get(msg).decode('UTF-8') + ' times.')
	except (IndexError, ValueError):
		update.message.reply_text('Usage: /add <keyword>')

# lab_4_writeup_question_3_part_2, not work cause the command handler or prefix handler. 
# def hello_kevin(update: Update, context: CallbackContext) -> None:
# 	update.message.reply_text('Good day, Kevin!')
		

def equiped_chatgpt(update, context):
	global chatgpt
	# lab_4_writeup_question_3
	if update.message.text == "hello Kevin":
		context.bot.send_message(chat_id=update.effective_chat.id, text="Good day, Kevin!")
	else:
		reply_message = chatgpt.submit(update.message.text)
		logging.info("Update: " + str(update))
		logging.info("context: " + str(context))
		context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)



if __name__=='__main__':
	main()
	
