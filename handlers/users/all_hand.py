from aiogram import types
from aiogram.types import CallbackQuery

from loader import vip
from filters import IsPrivate
from keyboards import close_markup, main_menu
from data import AdminButtons


@vip.callback_query_handler(text="...", state="*")
async def processing_missed_callback(call: CallbackQuery):
    await call.answer(cache_time=60)


@vip.message_handler(IsPrivate())
async def processing_missed_messages(msg: types.Message):
    if msg.text in await AdminButtons().btn_menu_list():
        info = await AdminButtons().info_buttons(msg.text)
        with open(f'utils/photos/{info[2]}.jpg', 'rb') as photo:
            await msg.answer_photo(
                photo=photo,
                caption=info[1],
                reply_markup=close_markup()
            )
