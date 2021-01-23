import random

import telebot
from PIL import Image 

from bot_info import token
from photo_filters import filters, filters_names

bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('send original photo')
keyboard.add(*filters_names)

compliments = [
	'Сool photo!', 'Great photo!', 'Wonderful photo!',
	'Very nice!', 'Very cute!', 'So beautiful!', 'Perfectly'
]

sticker = 'CAACAgEAAxkBAAEBxGhgAAGc58JpEhCUbrABihYG43gnOzcAAhEIAALjeAQAAVMCFqdk5ODcHgQ'


@bot.message_handler(commands=['start'])
def start_message(message):
	text = '\nIs\'s a bot for image processing. Send your photo.'
	bot.send_message(
		message.chat.id, reply_markup=keyboard,
		text=f'Hello, {message.from_user.first_name}!\n{text}')


@bot.message_handler(content_types=['photo'])
def image_message(message):
	img_file = bot.get_file(message.photo[-1].file_id)
	downloaded_file = bot.download_file(img_file.file_path)

	with open(f'users_images/{message.chat.id}.jpg', 'wb') as file:
		file.write(downloaded_file)

	try:
		bot.send_sticker(message.chat.id, sticker)
	except:
		pass


@bot.message_handler(content_types=['text'])
def text_message(message):
	if get_user_photo(message.chat.id):
		if message.text.lower() == 'send original photo':
			result_photo = get_user_photo(message.chat.id)
		elif message.text.lower() in filters_names:
			result_photo = photoshop_filter(message.chat.id, message.text.lower())
		else:
			bot.send_message(
				message.chat.id, text='Incorrect filter name 💣',
				reply_markup=keyboard)
			return 

		bot.send_photo(
			message.chat.id, result_photo,
			caption=random.choice(compliments)+'😍')
	else:
		bot.send_message(
			message.chat.id, text='You must send a photo for processing',
			reply_markup=keyboard)


def get_user_photo(user_id):
	try:
		return Image.open(f'users_images/{user_id}.jpg')
	except FileNotFoundError:
		return None


def photoshop_filter(user_id, photo_filter):
	image = get_user_photo(user_id)
	width, height = image.size

	for x in range(width):
		for y in range(height):
			R, G, B = image.getpixel((x, y))
			image.putpixel((x, y), filters[photo_filter](R, G, B))
	return image


bot.polling()