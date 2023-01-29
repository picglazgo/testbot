from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import vip
from states import CreatePromo
from data import AdmPromo


@vip.message_handler(state=CreatePromo.name)
async def create_promo(msg: types.Message, state: FSMContext):
	promo_name = msg.text

	if promo_name != '-':
		async with state.proxy() as data:
			data['name'] = promo_name

		await msg.answer(
			text='Введи награду промокода'
		)
		await CreatePromo.next()
	else:
		await state.finish()
		await msg.answer(
			text='Отменено')


@vip.message_handler(state=CreatePromo.money)
async def create_promo2(msg: types.Message, state: FSMContext):
	amount = msg.text
	if amount.isdigit():
		async with state.proxy() as data:
			data['money'] = amount
		await msg.answer(
			text='Введи колличество активаций'
		)
		await CreatePromo.next()
	else:
		await state.finish()
		await msg.answer(
			text='Отменено, сумма должна быть из цифр'
		)


@vip.message_handler(state=CreatePromo.amount)
async def create_promo3(msg: types.Message, state: FSMContext):
	amount = msg.text
	if amount.isdigit():
		async with state.proxy() as data:
			name = data['name']
			money = data['money']

		await msg.answer(
			text=f'<b>Промокод успешно создан!</b>\n\n'
				 f'<b>Название:</b> <code>{name}</code>\n\n'
				 f'<b>Награда:</b> <code>{money}</code>\n\n'
				 f'<b>Активаций:</b> <code>{amount}</code>')
		await AdmPromo().add_promo(name, money, amount)
		await state.finish()
	else:
		await state.finish()
		await msg.answer(
			text='Отменено, сумма должна быть из цифр'
		)
