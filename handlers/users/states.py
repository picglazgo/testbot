import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import User, Promocode
from keyboards import close_markup, authorize_markup2, authorize_markup1
from keyboards.inline.user_menu import return_cabinet_markup
from loader import vip, bot
from states import ActivatePromo, BuyCheating
from utils import config, SMMPanelAPI, SMMPanel





@vip.message_handler(state=BuyCheating.count)
async def cheat_link_states(msg: types.Message, state: FSMContext):
	if msg.text.isdigit():
		async with state.proxy() as data:
			service = data['service']
			cheat_type = data['type']
			order = data['order']

		orders = SMMPanel().cheat.get(f'{service}').get(cheat_type)
		order_info = orders.get(order)
		if int(order_info.get('min')) <= int(msg.text) <= int(order_info.get('max')):
			async with state.proxy() as data:
				data['count'] = msg.text
			price = float(order_info.get('price')) * int(msg.text)

			await msg.answer(
				text=f"<b>📛 Важно!</b>\n"
					 f"<b>Вводить правильно ссылку на нужный вам вид услуги! "
					 f"При неправильном вводе - у вас пропадают деньги!</b>\n\n"
					 f"<b>💈 Cервис:</b> {SMMPanel().cheat_service_name(service)} {SMMPanel().cheat_type_name(cheat_type)}\n"
					 f"<b>🧿 Название:</b> {order_info.get('name')}\n"
					 f"<b>🧿 Количество:</b> {msg.text}\n"
					 f"<b>🧿 Количество:</b> {msg.text}\n"
					 f"<b>💳 Цена:</b> {price} RUB"
			)
			await msg.answer(
				text='<b>Введите ссылку:</b>'
			)
			await BuyCheating.next()
		else:
			await msg.answer(
				text=f'Не правильное количество!\nДоступно: от {order_info.get("min")} до {order_info.get("max")}'
			)
			await state.finish()
	else:
		await msg.answer(
			text=f'Количество нужно вводить в числах!'
		)
		await state.finish()


@vip.message_handler(state=BuyCheating.link)
async def cheat_link_states(msg: types.Message, state: FSMContext):
	link = re.search("(?P<url>https?://[^\s]+)", msg.text)
	if link is not None:
		link = link.group()

		async with state.proxy() as data:
			data['link'] = link

		await msg.answer(
			text=f'Ссылка для услуги: {link}, верно?\n Для подтверждения отправьте "+"'
		)
		await BuyCheating.next()
	else:
		await state.finish()
		await msg.answer(
			text='Это не ссылка!'
		)


@vip.message_handler(state=BuyCheating.confirm)
async def cheat_confirm(msg: types.Message, state: FSMContext):
	if msg.text.startswith("+"):
		async with state.proxy() as data:
			service = data['service']
			cheat_type = data['type']
			order = data['order']
			count = data['count']
			link = data['link']

		orders = SMMPanel().cheat.get(f'{service}').get(cheat_type)
		order_info = orders.get(order)
		price = float(order_info.get('price')) * int(count)
		service_price = float(order_info.get('price_service')) * int(count)

		if price <= float(User(msg.from_user.id).balance):
			order = await SMMPanelAPI().add_order(
				service_id=order,
				link=link,
				count=count
			)
			if order != 'no_balance':
				if order != 'no_order':
					await User(msg.from_user.id).updateBalance(-price)
					await msg.answer(
						text=f"<b>Ваш заказ выполняется!</b>\n"
							 f"<b>Услуга:</b>  {SMMPanel().cheat_service_name(service)} {SMMPanel().cheat_type_name(cheat_type)} | {order_info.get('name')}"
							 f"<b>Колличество:</b> {count}",
						reply_markup=close_markup()
					)
					await bot.send_message(
						chat_id=config.config('admin_group'),
						text=f"<b>Куплена накрутка!</b>\n\n"
							 f"<b>💈 Cервис:</b> {SMMPanel().cheat_service_name(service)} {SMMPanel().cheat_type_name(cheat_type)}\n"
							 f"<b>🧿 Название:</b> {order_info.get('name')}\n"
							 f"<b>🧿 Количество:</b> {count}\n"
							 f"<b>💳 Цена:</b> {price} RUB\n"
							 f"<b>Покупатель:</b> {msg.from_user.get_mention()} | {msg.from_user.id}\n"
							 f"<b>Куда:</b> {link}",
						disable_web_page_preview=True
					)
					await SMMPanel().cheat_logs(
						user_id=msg.from_user.id,
						service=service,
						service_name=SMMPanel().cheat_service_name(service),
						cheat_type=cheat_type,
						order_id=order,
						order_name=order_info.get('name'),
						link=link,
						count=count,
						price_service=service_price,
						price=price
					)
				else:
					print(order)
					await msg.answer(
						text='<b>Tехнические неполадки, попробуйте позже или напишите в поддержку</b>\n\n'
							 'Возможно на эту ссылку уже стоит заказ - нужно подождать'
					)
			else:
				await msg.answer(
					text='<b>Tехнические неполадки, попробуйте позже или напишите в поддержку</b>\n\n'
						 'Возможно на эту ссылку уже стоит заказ - нужно подождать'
				)
				await bot.send_message(
					chat_id=config.config('admin_group'),
					text=f'<b>Пополни баланс SMMPanel!\n'
						 f'Текущий баланс: {await SMMPanelAPI().get_balance()} RUB\n'
						 f'Покупка на {price} RUB</b>'
				)
		else:
			await msg.answer(
				text='<b>❌ У вас недостаточно средств, для покупки данного товара.</b>'
			)
	else:
		await msg.answer(
			text='<b>Действие отменено!</b>'
		)
	await state.finish()


@vip.message_handler(state=ActivatePromo.promo)
async def user_promo(msg: types.Message, state: FSMContext):
	promocode = Promocode(promo=msg.text)
	data = await promocode.getPromoList()
	stateData = await state.get_data()
	messageId = stateData['messageid']
	await msg.delete()
	print(data)
	
	if data is not None:
		if int(data[3]) > 0:
			if str(msg.from_user.id) not in data[4].split(','):
				await promocode.getActivatePromo(msg.from_user.id)
				await User(msg.from_user.id).updateBalance(float(data[2]))
				await msg.bot.edit_message_caption(chat_id=msg.chat.id, message_id=messageId, caption=f'''✅ <b>Промокод</b>
└<i>Введенный Вами промокод </i>«<b>123</b>»<i> успешно активирован! Вам начислено</i> <code>{msg.text}₽.</code>''', reply_markup=return_cabinet_markup())
				await msg.bot.send_message(
					chat_id=config.config('admin_group'),
					caption=f'<b>🎁 Активация промокода:</b>\n\n'
						 f'<b>Пользователь:</b> {msg.from_user.get_mention(as_html=True)} | {msg.from_user.id}\n\n'
						 f'<b>Промокод:</b> {msg.text} | <b>Сумма:</b> {data[2]} RUB', reply_markup=return_cabinet_markup()
				)
			else:
				await msg.bot.edit_message_caption(chat_id=msg.chat.id, message_id=messageId,
					caption=f'Вы уже активировали этот промокод', reply_markup=return_cabinet_markup()
				)
		else:
			await promocode.deletePromo()
			await msg.bot.edit_message_caption(chat_id=msg.chat.id, message_id=messageId,
				caption=f'Промокод закончился', reply_markup=return_cabinet_markup()
			)
	else:
		await msg.bot.edit_message_caption(chat_id=msg.chat.id, message_id=int(messageId),
			caption=f'''❌ <b>Промокод</b>
└<i>Введенный Вами промокод </i>«<b>{msg.text}</b>»<i>, не существует! Попробуйте еще раз..</i>''', parse_mode=types.ParseMode.HTML, reply_markup=return_cabinet_markup()
		)
