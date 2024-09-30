#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
import requests

from datetime import datetime
from decouple import config
from telegram import Update
from telegram.ext import (
	Application,
	CommandHandler,
	MessageHandler,
	filters,
	ContextTypes
)

TOKEN = config('BOT_ACCESS_TOKEN')
BOT_USERNAME = config('BOT_USERNAME')
LOG_HANDLER_NAME = config('BOT_LOG_NAME')
LOG_FILE_NAME = config('BOT_LOG_FILE_NAME')
OWNER = config('BOT_OWNER')
ENDPIONT_URL = config('BACKEND_URL')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	level=logging.INFO,
	handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE_NAME, mode='w')
    ]
)

logging.getLogger(LOG_HANDLER_NAME).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
	message_type: str = update.message.chat.type
	name: str = update.message.from_user.first_name
	telegram_id: int = update.message.from_user.id
	audience : str = update.message.from_user.username

	logger.info(f'User ({audience}) in {message_type} start a conversation.')

	if message_type == 'group':
		await update.message.reply_text("This bot doesn't serve in a group. Please remove it!")
	else:
		if audience == OWNER:
			try:
				response = requests.post(f"{ENDPIONT_URL}/create-account/", json={
					"name": name,
					"telegram_id": telegram_id,
					"username": audience
				})

				if response.status_code == 200:
					logger.info(f"User account created! {audience}.")
				elif response.status_code == 400:
					logger.info(f"User account exist! {audience} start again.")
				else:
					logger.error(f"Failed to create account: {response.json().get('detail', 'Unknown error')}")
			except requests.RequestException as e:
				logger.error(f'Error connecting to the FastAPI server when trying start a conversation with user: {str(e)}')

			await update.message.reply_text("""Hello there!
I am here to help you gather the information you need from all over the internet. For now, I am PRIVATE service. So please, dont send messages here for now!
Thanks""")
		else:
			return

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text("""You can use this bot like the structure below:\n
-Send URLs like a message. I will extract them and store them.""")

# Responses
def handle_response(text: str, telegram_id: int, entities: tuple) -> str:
	processed: str = text.lower()

	if entities:
		urls = []
		for item in entities:
			if item.type == 'url':
				urls.append(text[item.offset:item.offset+item.length])

		if urls:
			for item in urls:
				try:
					response = requests.post(f"{ENDPIONT_URL}/set-url/", json={
						"url": item,
						"telegram_id": telegram_id
					})

					if response.status_code == 200:
						logger.info(f"Url created! {item}.")
					else:
						logger.error(f"Failed to create url: {response.json().get('detail', 'Unknown error')}")
				except requests.RequestException as e:
					logger.error(f'Error connecting to the FastAPI server when trying add url: {str(e)}')
					return 'Internal Error. Please try again later!'
				
			return 'URL/URLs created!'
		else:
			return 'Just URL support!'
	elif 'hello' in processed:
		return 'Hey!'
	else:
		return "I didn't find any solution for what you send!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
	message_type: str = update.message.chat.type
	text: str = update.message.text
	audience : str = update.message.from_user.username
	telegram_id: int = update.message.from_user.id
	entities: tuple =  update.message.entities

	logger.info(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

	if message_type == 'group':
		if BOT_USERNAME in text:
			response: str = "This bot doesn't serve in a group. Please remove it!" 
		else:
			return
	else:
		if audience == OWNER:
			response: str = handle_response(text, telegram_id, entities)
		else:
			logger.warning(f'User {audience} send message!')
			response: str = "It is a PRIVATE server."

	logger.info('Bot: ' + response)
	await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
	logger.error(f'Update {update} caused error {context.error}')

def main() -> None:
	logger.info('Starting bot...')
	app = Application.builder().token(TOKEN).build()

	# Commands
	app.add_handler(CommandHandler('start', start_command))
	app.add_handler(CommandHandler('help', help_command))

	# Messages
	app.add_handler(MessageHandler(filters.TEXT, handle_message))

	# Errors
	app.add_error_handler(error)

	# Polls the bot
	logger.info('Polling...')
	app.run_polling(poll_interval=3)

if __name__ == '__main__':
	main()
