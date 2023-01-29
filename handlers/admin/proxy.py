from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import vip
from states import ProxyLineAPIAdd, ProxyPercent
from keyboards import inline as menu
from utils import config


@vip.callback_query_handler(text='edit_proxy_token')
async def admin_qiwi(call: types.CallbackQuery):
    await ProxyLineAPIAdd.api.set()
    await call.message.answer(
        text='Введите новый ProxyLine API:'
    )


@vip.message_handler(state=ProxyLineAPIAdd.api)
async def admin_qiwitoken(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api'] = msg.text

    await msg.answer(
        text='Отправьте "+", для подтверждения'
    )
    await ProxyLineAPIAdd.next()


@vip.message_handler(state=ProxyLineAPIAdd.confirm)
async def admin_qiwitoken_two(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            api = data['api']
        config.edit_config('proxy_api', api)
        await msg.answer(
            text='Успешно изменен ProxyLine API'
        )
    else:
        await msg.answer(
            text='Действие отменено!'
        )
    await state.finish()


@vip.callback_query_handler(text='edit_proxy_percent')
async def admin_qiwinumber(call: types.CallbackQuery):
    await ProxyPercent.percent.set()
    await call.message.answer(
        text='Введите новую наценку на прокси'
    )


@vip.message_handler(state=ProxyPercent.percent)
async def admin_qiwinumber_1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['percent'] = msg.text

    await msg.answer(
        text='Отправьте "+", для подтверждения'
    )
    await ProxyPercent.next()


@vip.message_handler(state=ProxyPercent.confirm)
async def admin_qiwinumber_two(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            percent = data['percent']
        config.edit_config('proxy_percent', percent)
        await msg.answer(
            text='Успешно изменена наценка на прокси',
            reply_markup=menu.close_markup()
        )
    else:
        await msg.answer(
            text='Действие отменено!'
        )
    await state.finish()
