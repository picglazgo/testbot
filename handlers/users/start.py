from aiogram import types
from aiogram.dispatcher import FSMContext

from data import User
from middlewares.throttling import rate_limit
from filters import IsPrivate, SubscribeFilter
from keyboards import main_menu, authorize_markup1
from loader import bot, vip
from utils import config

@rate_limit(limit=1)
@vip.message_handler(IsPrivate(), commands=['start'], state="*")
async def start_handler(msg: types.Message, state: FSMContext):
    await state.finish()
    status, invite, userStatus = await User().joinFromBot(
        user_id=msg.from_user.id,
        username=msg.from_user.username,
        who_invite=msg.text[7:]
    )
    if userStatus in ['step1', 'step2']:
        # Изменил тут

        # await msg.answer(
        #     text=f'<b>Добро Пожаловать</b> {msg.from_user.get_mention(as_html=True)}\n'
        #          f'<b>Я VIP Market</b>  - в моем ассортименте много полезного, чекай скорей!',
        #     reply_markup=main_menu()
        # )
        # await bot.send_message(
        #     chat_id=config.config('admin_group'),
        #     text=f'Новый пользователь {msg.from_user.get_mention()} | {msg.from_user.id}'
        # )
        # if invite != 0:
        #     await bot.send_message(
        #         chat_id=invite,
        #         text=f'У вас новый реферал: {msg.from_user.get_mention(as_html=True)} !')

        await msg.answer('''
🪪 <b>Авторизация:</b> 1<code>/2</code>

📄 <b>Перед использованием бота, Вам необходимо принять пользовательское соглашение.</b>
└https://telegra.ph/soglashenie-04-18-2
''', parse_mode=types.ParseMode.HTML, reply_markup=authorize_markup1(), disable_web_page_preview=True)
    else:
        if await SubscribeFilter().check(msg) is False:
            return

        if User(msg.from_user.id).ban == 'no' and SubscribeFilter():
            await msg.answer(
                text=f'''📍 <b>Добро пожаловать, </b><u>{msg.chat.first_name}</u>!

<b>ViMento Store</b> - <i>oдин из лучших и изобильных маркет-плейсов по продаже цифровых товаров. </i>

🎖️<b>Наши преимущества</b>
├<i>Огромный спектр эксклюзивных товаров под любые цели и нужды.</i>
├<i>Одни из самых приятных цен на рынке, ниже оптовых.</i>
├<i>Частые обновления и розыгрыши.</i>
├<i>Отзывчивая Администрация, с огромным багажем опыта работы с клиентами.</i>
├<i>Безупречная репутация, нам доверяют 1000-и пользователей.</i>
└<i>Простой и удобный интерфейс.</i>

🔘 <b>Статистика</b>
├<i>Совершенных заказов:</i> #<code>100000</code>
└<i>На сумму:</i> <code>100000₽</code>''', parse_mode=types.ParseMode.HTML, reply_markup=main_menu()
            )
