from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils import config
from data import User
import keyboards

class IsGroup(BoundFilter):

	async def check(self, message: types.Message):
		return message.chat.type in (types.ChatType.GROUP,
									 types.ChatType.SUPERGROUP)


class IsPrivate(BoundFilter):

	async def check(self, message: types.Message):
		return message.chat.type == types.ChatType.PRIVATE


class IsAdmin(BoundFilter):
	async def check(self, message: types.Message):
		return str(message.from_user.id) in config.config("admin_id")


class IsBan(BoundFilter):
	async def check(self, message: types.Message):
		if await User().checkFromBase(message.from_user.id):
			return User(message.from_user.id).ban != 'yes'
		else:
			return await User().checkFromBase(message.from_user.id)


class SubscribeFilter(BoundFilter):
	async def check(self, message):
		if isinstance(message, types.CallbackQuery):
			message = message.message
		
		user_channel_status = await message.bot.get_chat_member(chat_id='@testbotzaka3', user_id=message.chat.id)
		if user_channel_status["status"] != 'left':
			return True
		else:
			await User().updateStatus(message.chat.id, 'step2')
			await message.bot.send_message(message.chat.id, '❗️ Вы не подписаны на канал\n└@testbotzaka3', reply_markup=keyboards.authorize_markup2)
			return False