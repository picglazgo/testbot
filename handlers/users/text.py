from aiogram import types
from aiogram.dispatcher import FSMContext
import re

import requests

from loader import bot, vip
from filters import IsPrivate, IsBan
from data import (
    User,
    cabinet_msg,
    infomation
)
from keyboards import (
    cabinet_markup,
    main_menu,
    shop_menu_btn,
    infomation_markup
)
from utils import Catalog, BTCPayment

def convertToBtc(amount):
    res = requests.get('https://blockchain.info/ticker').json()
    result = round(float(amount) / res['RUB']['15m'] , 8) 
    return result

    
@vip.message_handler(IsPrivate(), IsBan(), text=shop_menu_btn[1], state="*")
async def message_one(msg: types.Message, state: FSMContext):
    await state.finish()
    user = User(msg.from_user.id)

    if user.purchases == 0:
        statusUser = '🥸 Новичок'
    elif user.purchases >= 1 and user.purchases <= 5:
        statusUser = '😎 Постоялец'
    elif user.purchases > 5:
        statusUser = '🤑 Скупщик'

    balanceBtc = convertToBtc(user.balance)
    await msg.answer_photo(
        photo='https://i.imgur.com/MTn479J.jpg',
        caption=cabinet_msg.format(
            user_id=msg.from_user.id,                                           
            login=msg.from_user.username,
            data=user.get_days(),
            balance=user.balance,
            status=statusUser,
            btcBalance=balanceBtc
        ),
        reply_markup=cabinet_markup(), parse_mode=types.ParseMode.HTML
    )


@vip.message_handler(IsPrivate(), IsBan(), text=shop_menu_btn[2], state="*")
async def message_two(msg: types.Message):
    await msg.answer(
        text=infomation,
        reply_markup=infomation_markup,
        parse_mode=types.ParseMode.HTML,
        disable_web_page_preview=True
    )


@vip.message_handler(IsPrivate(), IsBan(), text=shop_menu_btn[0], state="*")
async def message_three(msg: types.Message):
    await msg.answer_photo(
        caption='''🛒 <b>Каталог</b>
└<i>Выберите желаемую категорию:</i>''',
        photo='https://i.imgur.com/sKoCi7u.jpg',
        reply_markup=await Catalog().get_menu(),
    )


@vip.message_handler(IsPrivate(), IsBan(),
                     lambda message: re.search(r'BTC_CHANGE_BOT\?start=', message.text))
async def crypto_handler(msg: types.Message):
    await msg.answer(
        text='<b>♻️ Подождите...</b>'
    )
    await BTCPayment().receipt_parser(
        bot=bot,
        user_id=msg.from_user.id,
        cheque=msg.text
    )
