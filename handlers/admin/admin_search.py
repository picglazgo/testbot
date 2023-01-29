from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import vip, bot
from states import AdmSearch, AdminGiveBalance
from data import User
from keyboards import inline as menu


@vip.message_handler(state=AdmSearch.user_id)
async def adm_search2(msg: types.Message, state: FSMContext):
    if await User().checkFromBase(msg.text):
        user = User(msg.text)
        await bot.send_message(
            chat_id=msg.from_user.id,
            text=f'<b>👤 Пользователь:</b> @{user.username}\n\n'
                 f'<b>💳 Баланс:</b> <code>{user.balance}</code> <b>RUB</b>\n\n'
                 f'<b>⚙️ Статус:</b> <code>{user.status}</code>\n\n'
                 f'<b>♻️ Количество покупок:</b> <code>{user.purchases}</code>\n\n'
                 f'<b>💢 Бан:</b> <code>{user.ban}</code> (yes - значит в бане)\n\n'
                 f'<b>🕰 Дата регистрации:</b> <code>{user.date[:10]}</code>',
            reply_markup=menu.admin_user_menu(msg.text)
        )

    else:
        await msg.answer(
            text='💢 Я не нашел такого пользователя'
        )
    await state.finish()


@vip.message_handler(state=AdminGiveBalance.amount)
async def give_amount(msg: types.Message, state: FSMContext):
    if msg.text.isdecimal():
        async with state.proxy() as data:
            data['amount'] = msg.text

        await msg.answer(
            text='Введите "+" для подтверждения'
        )
        await AdminGiveBalance.next()
    else:
        await state.finish()
        await msg.answer(
            text='Ввведененное, не является числом'
        )


@vip.message_handler(state=AdminGiveBalance.confirm)
async def give_confirm(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            await User(data['user_id']).updateFullBalance(data['amount'])
        await msg.answer(
            text=f'Пользователю: @{User(data["user_id"]).username} обновлен баланс!'
        )
    else:
        await msg.answer(
            text='Действие отменено'
        )
    await state.finish()
