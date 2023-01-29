from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def stats_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Закрыть', callback_data=f'to_close'),

			]
		]
	)

	return markup


def admin_user_menu(user_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
                InlineKeyboardButton(text = 'Изменить баланс', callback_data = f'adm_give_balance:{user_id}'),
			],
			[
				InlineKeyboardButton(text = 'Забанить', callback_data = f'adm_ban:{user_id}'),
				InlineKeyboardButton(text = 'Разбанить', callback_data = f'adm_unban:{user_id}'),
			],
		]
	)

	return markup

def admin_sending():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✔️ Рассылка(только текст)', callback_data='email_sending_text'),
                InlineKeyboardButton(
                    text='✔️ Рассылка(текст + фото)', callback_data='email_sending_photo'),
            ],
            [
                InlineKeyboardButton(
                    text='Управление заплан. рассылками', callback_data='edit_down_sending'),
            ],
            [
                InlineKeyboardButton(
					text='Обновить меню', callback_data='email_sending_update'),
            ],
            [
                InlineKeyboardButton(
                    text='💢 Отмена', callback_data='to_closed'),
            ]
        ]
    )

    return markup

def admin_proxy_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = 'ИЗменить | Token', 
                                    callback_data = 'edit_proxy_token'),
                InlineKeyboardButton(text = 'ИЗменить | Наценку', 
                                    callback_data = 'edit_proxy_percent'),
			],
			[
				InlineKeyboardButton(text = '💢 Закрыть', 
                                    callback_data = 'to_close'),
			],
		]
	)

	return markup

def admin_btn_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Добавить кнопку', callback_data='admin_button_add'),
			],
			[
				InlineKeyboardButton(
					text='Активные кнопки', callback_data='admin_button_act'),
			],
		]
	)

	return markup

def adm_catalog_edit():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Активные каталоги', callback_data='adm_act_catalog'),
			],
			[
				InlineKeyboardButton(
					text='Создать каталог', callback_data='adm_create_catalog'),
			]
		]
	)

	return markup

def adm_catalog_info(catalog_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Изменить название', callback_data=f'edit_name_catalog:{catalog_id}')
			],
			[
				InlineKeyboardButton(
					text='Создать подкаталог', callback_data=f'create_subcatalog:{catalog_id}'),
			],
			[
				InlineKeyboardButton(
					text='Удалить каталог', callback_data=f'delete_catalog:{catalog_id}'),
			],
			[
				InlineKeyboardButton(
					text='Назад', callback_data='adm_act_catalog')
			]
		]
	)

	return markup


def adm_subcatalog_edit():
	markup = InlineKeyboardMarkup().add(
		InlineKeyboardButton(
			text='Активные подкаталоги', callback_data='adm_act_subcatalog'),
		InlineKeyboardButton(
			text='Создать подкаталог', callback_data='adm_create_subcatalog'),
	)

	return markup

def adm_subcatalog_info(catalog_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Изменить название', callback_data=f'edit_name_subcatalog:{catalog_id}')
			],
			[
				InlineKeyboardButton(
					text='Удалить подкаталог', callback_data=f'delete_subcatalog:{catalog_id}'),
			],
			[
				InlineKeyboardButton(
					text='Создать товар', callback_data=f'create_product:{catalog_id}'),
			],
			[
				InlineKeyboardButton(
					text='Назад', callback_data='adm_act_subcatalog'),
			],
		]
	)

	return markup

def adm_product_edit():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Активные товары', callback_data='adm_act_product'),
			],
			[
				InlineKeyboardButton(
					text='Создать товар', callback_data='adm_create_product'),
			]
		]
	)

	return markup

def adm_product_info(product_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Изменить название', callback_data=f'edit_name_product:{product_id}'),
				InlineKeyboardButton(
					text='Изменить описание', callback_data=f'edit_descr_product:{product_id}'),
			],
			[
				InlineKeyboardButton(
					text='Изменить цену', callback_data=f'edit_price_product:{product_id}'),
			],
			[
				InlineKeyboardButton(
					text='Загрузить товар', callback_data=f'download_product:{product_id}'),
				InlineKeyboardButton(
					text='Удалить товар', callback_data=f'delete_product:{product_id}'),
			],
			[
				InlineKeyboardButton(
					text='Назад', callback_data='adm_act_product'),
			],
		]
	)

	return markup

def adm_promo_info():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(
					text='Активные промо', callback_data='activ_promo'),
				InlineKeyboardButton(
					text='Создать промо', callback_data='create_promo'),
			],
			[ 
				InlineKeyboardButton(
					text='💢 Закрыть', callback_data='to_close')
			]
		]
	)

	return markup
