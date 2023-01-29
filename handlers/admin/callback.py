from aiogram import types
from aiogram.dispatcher import FSMContext


from loader import vip
from filters import IsAdmin
from keyboards import inline as menu
from data import User, proxy_stats, SendingMail, cheating_stats, \
    AdminButtons, AdmPromo
from states import AdminDownloadProduct, AdminGiveBalance, CreatePromo


@vip.callback_query_handler(IsAdmin(), text='proxy_stats')
async def proxy_statistic(call: types.CallbackQuery):
    await call.message.edit_text(
        text=await proxy_stats(),
        reply_markup=menu.close_markup()
    )


@vip.callback_query_handler(IsAdmin(), text='cheating_stats')
async def cheat_statistic(call: types.CallbackQuery):
    await call.message.edit_text(
        text=await cheating_stats(),
        reply_markup=menu.close_markup()
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='info_sending:')
async def admin_info_sending(call: types.CallbackQuery):
    text, markup = await SendingMail().down_sending_info(call.data.split(":")[1])
    await call.message.edit_text(text=text, reply_markup=markup)


@vip.callback_query_handler(IsAdmin(), text_startswith='del_sending:')
async def admin_del_sending(call: types.CallbackQuery):
    await SendingMail().del_sending(call.data.split(':')[1])
    await call.message.edit_text(text='Успешно удалено', reply_markup=menu.close_markup())


@vip.callback_query_handler(IsAdmin(), text_startswith='info_btn:')
async def admin_info_btn(call: types.CallbackQuery):
    text, markup = await AdminButtons().btn_info(call.data.split(":")[1])
    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='del_btn:')
async def admin_delete_btn(call: types.CallbackQuery):
    await AdminButtons().delete_button(call.data.split(":")[1])
    await call.message.edit_text(
        text='Кнопка удалена!'
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='adm_unban:')
async def adm_unban(call: types.CallbackQuery):
    await User(call.data.split(":")[1]).updateStatusBan("no")
    await call.message.answer(
        text='Пользователь разбанен',
        reply_markup=menu.close_markup()
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='adm_ban:')
async def adm_ban(call: types.CallbackQuery):
    await User(call.data.split(":")[1]).updateStatusBan("yes")
    await call.message.answer(
        text='Пользователь забанен',
        reply_markup=menu.close_markup()
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='adm_give_balance:')
async def adm_give(call: types.CallbackQuery, state: FSMContext):
    await AdminGiveBalance.amount.set()
    async with state.proxy() as data:
        data['user_id'] = call.data.split(":")[1]

    await call.message.answer(
        text='Введите значение, на которое изменится баланс пользователя:'
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='download_product:')
async def adm_add_product(call: types.CallbackQuery, state: FSMContext):
    await AdminDownloadProduct.file.set()
    async with state.proxy() as data:
        data['product_id'] = call.data.split(":")[1]
    await call.message.answer(
        text='Пришлите файл с товаром, я загружу его'
    )


@vip.callback_query_handler(IsAdmin(), text='create_promo')
async def admin_create_promo(call: types.CallbackQuery):
    await CreatePromo.name.set()
    await call.message.answer(
        text='Введи название промокода, который хочешь создать, для отмены введи "-", без ковычек:'
    )


@vip.callback_query_handler(IsAdmin(), text='activ_promo')
async def active_promocode(call: types.CallbackQuery):
    markup = await AdmPromo().activ_promo_menu()
    await call.message.edit_text(
        text='Активные промокоды',
        reply_markup=markup
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='adm_promo:')
async def info_promocode(call: types.CallbackQuery):
    promo_id = call.data.split(":")[1]
    text, markup = await AdmPromo().get_info_promo(promo_id)
    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='promo_delete:')
async def delete_promocode(call: types.CallbackQuery):
    await AdmPromo().delete_promocode(call.data.split(":")[1])
    await call.message.delete()
    await call.message.answer(
        text='Промокод удален!',
        reply_markup=menu.close_markup()
    )
