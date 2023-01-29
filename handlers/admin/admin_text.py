from aiogram import types

from loader import vip
from filters import IsAdmin, IsPrivate
from data import admin_stats
from keyboards import inline as menu, defaut as key
from states import AdmSearch
from utils import config, ProxyLine


@vip.message_handler(IsAdmin(), IsPrivate(), commands=['admin', 'a', 'panel'], state="*")
async def admin_handler(msg: types.Message):
	await msg.answer(
		text='Открыта панель админа',
		reply_markup=key.admin_markup()
	)


@vip.message_handler(IsAdmin(), IsPrivate(), text=key.admin_button[0], state="*")
async def admin_statistic(msg: types.Message):
	await msg.answer(
		text=await admin_stats(),
		reply_markup=menu.stats_markup()
	)


@vip.message_handler(IsAdmin(), IsPrivate(), text=key.admin_button[1], state="*")
async def admin_sending(msg: types.Message):
	await msg.answer(
		text='Выберите действие',
		reply_markup=menu.admin_sending()
	)


@vip.message_handler(IsAdmin(), IsPrivate(), text=key.admin_button[2], state="*")
async def admin_settings(msg: types.Message):
	await msg.answer(
		text='Вы перешли в настройки',
		reply_markup=key.admin_settings()
	)


@vip.message_handler(IsAdmin(), IsPrivate(), text=key.admin_button[3], state="*")
async def admin_search(msg: types.Message):
	await AdmSearch.user_id.set()
	await msg.answer(
		text='<b>Введите айди пользователя:</b>'
	)


@vip.message_handler(IsAdmin(), IsPrivate(), text=key.admin_button[4], state="*")
async def admin_exit(msg: types.Message):
	await msg.answer(
		'Вы перешли в главное меню',
		reply_markup=key.main_menu()
	)


@vip.message_handler(IsAdmin(), IsPrivate(), text=key.admin_settings_btn[0], state="*")
async def admin_buttons(msg: types.Message):
	await msg.answer(
		text='Выберите действие',
		reply_markup=menu.admin_btn_markup()
	)


@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[1])
async def admin_proxy(msg: types.Message):
	await msg.answer(
		text=f"""
<b>Данные по ProxyLine:</b>
<b>Баланс:</b> {await ProxyLine().get_balance()} RUB

<b>Наценка:</b> {config.config('proxy_percent')} %
<b>ProxyLine API:</b> {config.config('proxy_api')}
    """,
		reply_markup=menu.admin_proxy_markup()
	)


@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[2])
async def admin_catalog(msg: types.Message):
	await msg.answer(
		text='Выберите нужно вам действие:',
		reply_markup=menu.adm_catalog_edit()
	)


@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[3])
async def admin_catalog(msg: types.Message):
	await msg.answer(
		text='Выберите нужно вам действие:',
		reply_markup=menu.adm_subcatalog_edit()
	)


@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[4])
async def admin_catalog(msg: types.Message):
	await msg.answer(
		text='Выберите нужно вам действие:',
		reply_markup=menu.adm_product_edit()
	)


@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[5])
async def admin_promocode(msg: types.Message):
	await msg.answer(
		text='Выберите нужно вам действие:',
		reply_markup=menu.adm_promo_info()
	)
