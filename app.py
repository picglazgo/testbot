from aiogram import executor
import asyncio

from loader import vip
import handlers, middlewares
from utils import logger, QiwiPay
from handlers.admin.admin_sending import sending_checked


async def startup(dp):
	asyncio.create_task(QiwiPay().wait_pays_qiwi(dp.bot, 10))
	asyncio.create_task(sending_checked(10, dp.bot))

if __name__ == '__main__':
	logger.debug('VIP Market | Started')
	executor.start_polling(vip, on_startup=startup)
