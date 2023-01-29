from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import config


def projects_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='📣 Канал', url='https://t.me/END_Soft'),
				InlineKeyboardButton(
					text='💭 Чатик', url='https://t.me/end_chat'),
			],
			[
				InlineKeyboardButton(
					text='🛒 Вирт Номера', url='https://t.me/VIP_SMS_BOT'),
			],
			[
				InlineKeyboardButton(
					text='🤝 Услуги', url='https://t.me/VIPMarketChat')
			]
		]
	)

	return markup


def cabinet_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='⤵️ Пополнить', callback_data='payments'),
				InlineKeyboardButton(
					text='🎁 Промокод', callback_data='promocode'),
			],
			[
				InlineKeyboardButton(
					text='👫 Реферальная система', callback_data='referral'),
			],
			[
				InlineKeyboardButton(
					text='🛍️ Мои покупки', callback_data='my_purchases'),
			]
		]
	)

	return markup


def refereals_markup():
	markup = InlineKeyboardMarkup().add(
		InlineKeyboardButton('👬 Рефералы', callback_data='referalls'),
		InlineKeyboardButton('💸 Вывод', callback_data='withdrawRef'),
	).add(
		InlineKeyboardButton('Назад', callback_data='return_to_cabinet')
	)
	return markup


def withdrawRef_markup():
	markup = InlineKeyboardMarkup().add(
		InlineKeyboardButton('💳 Реквизиты', callback_data='rekveziti'),
		InlineKeyboardButton('🤖 Баланс бота', callback_data='balanceBota')
	).add(
		InlineKeyboardButton('Назад', callback_data='return_to_cabinet')
	)
	return markup
	

def purchases_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='🛒 Купленные товары', callback_data='my_product_order'),
			],
			[
				InlineKeyboardButton(
					text='Назад', callback_data='return_to_cabinet'),
			]
		]
	)

	return markup


def return_cabinet_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='Назад', callback_data='return_to_cabinet'),
			]
		]
	)
	return markup


def payment_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='💳 Banker | Chatex | ETH', callback_data='pay_btc'),
			],
			[
				InlineKeyboardButton(
					text='Назад', callback_data='return_to_cabinet'),
			],
		]
	)

	return markup


def close_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='💢 Понятно', callback_data='to_close'),
			],
		]
	)

	return markup


def pay_qiwi_markup(url):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='♻️ Перейти к оплате ♻️', url=url)
			]
		]
	)

	return markup

# Добавил инлайн кнопки 

def authorize_markup1():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🔍 Прочитать', url='https://telegra.ph/soglashenie-04-18-2'),
				InlineKeyboardButton('✅ Принять', callback_data='acceptAuth1')
			]
		]
	)

	return markup



authorize_markup2 = InlineKeyboardMarkup().add(
	InlineKeyboardButton(text='Подписаться', url='https://t.me/testbotzaka3'),
	InlineKeyboardButton('✅ Подписался', callback_data='acceptAuth2')
)


infomation_markup = InlineKeyboardMarkup().add(
	InlineKeyboardButton('📍 Наши проекты', url="https://t.me/analbeks"),
).add(
	InlineKeyboardButton('👨‍💻 Поддержка', url="https://t.me/analbeks"),
	InlineKeyboardButton('💬 Отзывы', url="https://t.me/analbeks")
).add(
	InlineKeyboardButton('📰 Новостной канал', url="https://t.me/analbeks")
)