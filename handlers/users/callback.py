import datetime
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
import os

import requests
from data.functions.referal import Referals
from keyboards.inline.user_menu import refereals_markup, withdrawRef_markup

from loader import bot, vip
from filters import IsBan, SubscribeFilter
from keyboards import (
    close_markup,
    pay_qiwi_markup,
    payment_markup,
    projects_markup,
    cabinet_markup,
    return_cabinet_markup,
    purchases_markup,
    authorize_markup2,
    main_menu
)
from data import (
    rules,
    User,
    btc_pay,
    pay_qiwi,
    product,
    access_purchase,
    cabinet_msg,
    refferal,
    refWithdraws,
    adm_product,
)
from states.market import ProductCount
from utils import (
    config,
    Catalog,
    SubCatalog,
    Product,
    Proxy,
    QiwiPay,
    SMMPanel
)
from states import ActivatePromo, BuyCheating
from utils.market import notificationProduct

async def isSubscribed(bot: types.Message.bot, chatid, channelId):
    user_channel_status = await bot.get_chat_member(chat_id=channelId, user_id=chatid)
    if user_channel_status["status"] != 'left':
        return True
    else:
    	return False

async def cropProduct(caption):
    caption = re.sub('├<i>В наличии:</i> <code>\d\sшт\.</code>\n', '', caption)
    caption = caption.split('├<i>К покупке:')[0] + caption.split('├<i>К покупке:')[1].split('</code>\n', 1)[1]
    return caption

@vip.callback_query_handler(text='acceptAuth1')
async def authorizeStep1(call: types.CallbackQuery):
    message = call.message
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await User().updateStatus(message.from_id, 'step2')
    await call.bot.send_message(message.chat.id, '''
🪪 <b>Авторизация:</b> 2<code>/2</code>

📰 <b>Перед использованием бота, Вам необходимо подписаться на наш канал.</b>
└@testbotzaka3
''', reply_markup=authorize_markup2, parse_mode=types.ParseMode.HTML)


@vip.callback_query_handler(text='acceptAuth2')
async def authorizeStep2(call: types.CallbackQuery):
    message = call.message
    subscribe = await isSubscribed(call.bot, message.chat.id, '@testbotzaka3')
    if subscribe:
        await call.bot.delete_message(call.message.chat.id, call.message.message_id)
        await User().updateStatus(message.chat.id, 'User')
        await call.bot.send_message( 
            chat_id=message.chat.id,
            text=f'''📍 <b>Добро пожаловать, </b><u>{message.chat.first_name}</u>!

<b>ViMento Store</b> - <i>oдин из лучших и изобильных маркет-плейсов по продаже цифровых товаров. </i>

🎖️<b>Наши преимущества</b>
├<i>Огромный спектр эксклюзивных товаров под любые цели и нужды.</i>
├<i>Одни из самых приятных цен на рынке, ниже оптовых.</i>
├<i>Частые обновления и розыгрыши.</i>
├<i>Отзывчивая Администрация, с огромным багажем опыта работы с клиентами.</i>
├<i>Безупречная репутация, нам доверяют 1000-и пользователей.</i>
└<i>Простой и удобный интерфейс.</i>

🔘 <b>Статистика</b>
├<i>Совершенных заказов:</i> #1000
└<i>На сумму:</i> 100000₽''', parse_mode=types.ParseMode.HTML, reply_markup=main_menu()
            )
    else:
        await call.answer('❗️ Вы не подписаны на канал', show_alert=True)
        
            

@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='rules_market')
async def rules_handler(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text=rules,
        reply_markup=close_markup()
    )
    await call.answer()


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='our_projects')
async def our_project(call: types.CallbackQuery):
    await call.message.edit_reply_markup(
        reply_markup=projects_markup()
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='payments')
async def payments_handler(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption='<b>💳 Выбери способ пополнения:</b>',
        reply_markup=payment_markup()
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='pay_btc')
async def pay_btc_handler(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption=btc_pay,
        reply_markup=close_markup()
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='pay_qiwi')
async def pay_qiwi_handler(call: types.CallbackQuery):
    url, code, phone = await QiwiPay().deposit_qiwi(
        call.from_user.id
    )
    text = pay_qiwi.format(
        number=phone,
        code=code
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=pay_qiwi_markup(
            url=url
        )
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='to_close')
async def close_message_handler(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='to_catalog')
async def to_catalog_handler(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption=f'''🛒 <b>Каталог</b>
└<i>Выберите желаемую категорию:</i>''',
        reply_markup=await Catalog().get_menu(),
        parse_mode=types.ParseMode.HTML
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='catalog:')
async def catalog_handler(call: types.CallbackQuery):
    category_id = call.data.split(":")[1]
    catalog = await Catalog().get_category(category_id)
    markup = await SubCatalog().get_subcategory_menu(category_id)
    await call.message.edit_caption(caption=f'''🛒 <b>Каталог</b>
├<i>Категория:</i> «<code>{catalog[1]}</code>»
└<i>Выберите желаемую под-категорию:</i>''', parse_mode=types.ParseMode.HTML, reply_markup=markup)




# @vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='catalog:')
# async def catalog_handler(call: types.CallbackQuery):
#     user = User(call.from_user.id)
#     text = f'<b>💳 Баланс:</b> {user.balance} RUB\n<b>🛍 Выберите категорию:</b>'

#     markup = await SubCatalog().get_subcategory_menu(
#         category_id=call.data.split(":")[1]
#     )

#     for ы

#     await call.message.edit_caption(
#         caption=text,
#         reply_markup=markup
#     )
#     await call.answer()


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='subcatalog:')
async def subcatalog_handler(call: types.CallbackQuery):
    subcatalog = await SubCatalog().get_subcategory(call.data.split(":")[1])
    category = await Catalog().get_category(subcatalog[2].replace('c_', ''))
    products = await Product().get_product_menu(call.data.split(":")[1])
    await call.message.edit_caption(f'''🛒 <b>Каталог</b>
├<i>Категория:</i> «<code>{category[1]}</code>»
├<i>Под-категория:</i> «<code>{subcatalog[1]}</code>»
└<i>Выберите желаемый товар:</i>''', parse_mode=types.ParseMode.HTML, reply_markup=products)


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='disableNotificationProduct:')
async def disableNotificationProduct(call: types.CallbackQuery):
    name = call.data.split(':')[1]
    user = User(call.from_user.id)
    info = await Product().getByName(call.data.split(":")[1])
    products = await Product().get_amount_products(
        product_id=call.data.split(":")[1]
    )

    markup = await Product().buy_product_markup(
        product_id=call.data.split(":")[1]
    )
    subcatalog = await SubCatalog().get_subcategory(info[0][1])
    catalog = await Catalog().get_category(subcatalog[2])
    await notificationProduct().deleteRowByName(name, call.message.chat.id)
    caption=product.format(
        subcategory=subcatalog[1],
        catalog=catalog[1],
        name=info[0][2],
        price=info[0][3],
        balance=User(call.from_user.id).balance,
        description=info[0][4],
        amount_product=products,
        btcBalance=await user.getBtcBalance()
    )
    



    if products == 0:
        caption = await cropProduct(caption)
        caption = caption.split('💰')[0]
        caption += '📭 <b>К сожалению, данный товар закончился, но Вы можете включить оповещения о пополнении, по кнопке ниже. Мы уведомим Вас, сразу же как товар появятся у нас в наличии.</b>'
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('📨 Оповестить о наличии', callback_data='notificationProduct:' + str(info[0][0])),
        ).add(
            types.InlineKeyboardButton('Назад', callback_data='to_catalog')
        )

    await call.message.edit_caption(
        caption=caption,
        reply_markup=markup,
        parse_mode="HTML"
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='notificationProduct:')
async def notificationProductHandler(call: types.CallbackQuery):
    user = User(call.from_user.id)
    product = await Product().get_product(
        product_id=call.data.split(":")[1]
    )
    products = await Product().get_amount_products(
        product_id=call.data.split(":")[1]
    )
    subcatalog = await SubCatalog().get_subcategory(product[1])
    catalog = await Catalog().get_category(subcatalog[2])
    await notificationProduct().createNotifiction(product[2], call.from_user.id)
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('❌ Выключить оповещения', callback_data='disableNotificationProduct:'+product[2]),
    ).add(
        types.InlineKeyboardButton('Назад', callback_data='subcatalog:' + subcatalog[0])
    )

    await call.message.edit_caption(
        caption=await cropProduct(adm_product.format(
            catalog=catalog[1],
            name=product[2],
            price=product[3],
            balance=User(call.from_user.id).balance,
            description=product[4],
            amount_product=products,
            btcBalance=await user.getBtcBalance()
        ) + '└<i>Оповещения о наличии:</i> ✅ <code>Включены</code>'),
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='product:', state="*")
async def product_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = User(call.from_user.id)
    info = await Product().get_product(
        product_id=call.data.split(":")[1]
    )
    products = await Product().get_amount_products(
        product_id=call.data.split(":")[1]
    )

    markup = await Product().buy_product_markup(
        product_id=call.data.split(":")[1]
    )
    if 'deleteBack' in call.data:
        markup.inline_keyboard[-1].pop()

    subcatalog = await SubCatalog().get_subcategory(info[1])
    catalog = await Catalog().get_category(subcatalog[2])
    caption=product.format(
        subcategory=subcatalog[1],
        catalog=catalog[1],
        name=info[2],
        price=info[3],
        balance=User(call.from_user.id).balance,
        description=info[4],
        amount_product=products,
        btcBalance=await user.getBtcBalance()
    )

    haveBind = await notificationProduct().haveBind(info[0][2], call.from_user.id)

    if products == 0 and haveBind is False:
        caption = await cropProduct(caption)
        caption = caption.split('💰')[0]

        caption += '📭 <b>К сожалению, данный товар </b><ins>закончился</ins><b>, но Вы можете включить оповещения о пополнении, по кнопке ниже. Мы уведомим Вас, сразу же как товар появятся у нас в наличии.</b>'
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('📨 Оповестить о наличии', callback_data='notificationProduct:' + str(info[0][0])),
        ).add(
            types.InlineKeyboardButton('Назад', callback_data='to_catalog')
        )


    if haveBind:
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('❌ Выключить оповещения', callback_data='disableNotificationProduct:'+info[2]),
        ).add(
            types.InlineKeyboardButton('Назад', callback_data='subcatalog:' + subcatalog[0])
        )


        caption=await cropProduct(adm_product.format(
            catalog=catalog[1],
            name=info[2],
            price=info[3],
            balance=User(call.from_user.id).balance,
            description=info[4],
            amount_product=products,
            btcBalance=await user.getBtcBalance()
        ) + '└<i>Оповещения о наличии:</i> ✅ <code>Включены</code>')


    if 'notCaption' in call.data:
        return await call.message.edit_text(
            text=caption,
            reply_markup=markup,
            parse_mode=types.ParseMode.HTML
        ) 

    await call.message.edit_caption(
        caption=caption,
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='deleteMessage')
async def deleteMessage(call: types.CallbackQuery):
    await call.message.delete()
    await notificationProduct().deleteRowByName(call.data.split(':')[1], call.from_user.id)


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='product_buy:')
async def product_buy_handler(call: types.CallbackQuery, state: FSMContext):
    user = User(call.from_user.id)
    products = await Product().get_amount_products(
        product_id=call.data.split(":")[1]
    )
    if int(products) > 0:
        markup = await Product().get_buy_menu(
            product_id=call.data.split(":")[1],
            productCount=products
        )
        info = await Product().get_product(
            product_id=call.data.split(":")[1]
        )
        productCount = await Product().get_amount_products(info[0][0])
        subcatalog = await SubCatalog().get_subcategory(info[1])
        catalog = await Catalog().get_category(subcatalog[2])
        await call.message.edit_caption(
            caption=product.format(
                subcategory=subcatalog[1],
                catalog=catalog[1],
                name=info[2],
                price=info[3],
                balance=User(call.from_user.id).balance,
                description=info[4],
                amount_product=products,
                btcBalance=await user.getBtcBalance()
            ) + f'\n🧮 <b>Введите, либо выберите желаемое число товара от 1 до {str(productCount)}, на покупку:</b>',
            reply_markup=markup, parse_mode=types.ParseMode.HTML
        )
        await ProductCount.count.set()
        async with state.proxy() as data:
            data['id'] = call.data.split(":")[1]
            data['messageid'] = call.message.message_id
    else:
        await call.answer(
            text='Товара нет в наличии, попробуй позже...'
        )




@vip.message_handler(state=ProductCount.count)
async def product_count(message: types.Message, state: FSMContext):
    count = message.text
    stateData = await state.get_data()
    user = User(message.chat.id)
    await message.delete()
    product_id = stateData['id']
    info = await Product().get_product(stateData['id'])
    productCount = await Product().get_amount_products(product_id)
    markup = await Product().get_buy_menu(
        product_id=product_id,
        productCount=productCount
    )
    print(markup)
    if count.isdigit() is False or (count.isdigit() and productCount < int(count)) or (count.isdigit() and int(count) <= 0):

        subcatalog = await SubCatalog().get_subcategory(info[0][1])
        catalog = await Catalog().get_category(subcatalog[2])
        await message.bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=stateData['messageid'],
            caption=product.format(
                subcategory=subcatalog[1],
                catalog=catalog[1],
                name=info[0][2],
                price=info[0][3],
                balance=user.balance,
                description=info[0][4],
                amount_product=productCount,
                btcBalance=await user.getBtcBalance()
            ) + f'\n❌ <b>Вы ввели некорректное число. Еще раз введите, либо выберите желаемое число товара от 1 до {productCount}, на покупку:</b>',
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup
        )
    else:
        count = int(count)
        await state.finish()
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('💰 Купить', callback_data='buy_product:'+product_id+':'+str(count)),
        ).add(
            types.InlineKeyboardButton('❌ Отменить', callback_data='to_catalog')
        ).add(
            types.InlineKeyboardButton('Назад', callback_data='product:'+product_id)
        )
        info = await Product().get_product(product_id)
        subcatalog = await SubCatalog().get_subcategory(info[0][1])
        catalog = await Catalog().get_category(subcatalog[2])
        await message.bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=stateData['messageid'],
            caption=product.format(
                subcategory=subcatalog[1],
                catalog=catalog[1],
                name=info[0][2],
                price=info[0][3],
                balance=user.balance,
                description=info[0][4],
                amount_product=productCount,
                btcBalance=await user.getBtcBalance()
            ) + f'\n❓ <b>Вы уверены, что желаете приобрести данный товар в количестве: {count} шт.</b>',
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup
        )

        




@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='buy_menu_update:', state='*')
async def buy_menu_update_handler(call: types.CallbackQuery):
    products = await Product().get_amount_products(
        product_id=call.data.split(":")[1]
    )
    product_id, amount = call.data.split(":")[1], int(call.data.split(":")[2])
    price, update = call.data.split(":")[3], int(call.data.split(":")[4])
    
    if (amount + update) > 0:
        if (amount + update) <= 25:
            if products >= amount + update:
                markup = await Product().get_buy_menu(
                    product_id=product_id,
                    amount=amount,
                    price=price,
                    update=update,
                    productCount=products
                )
                await call.message.edit_reply_markup(
                    reply_markup=markup
                )
            else:
                await call.answer(
                    text='❗️ Данного количества нет в наличии', show_alert=True
                )
        else:
            await call.answer(
                text='❕ Максимально за раз можно купить 25 шт', show_alert=True
            )
    else:
        await call.answer(
            text='❗️ Минимальное количество для покупки 1 шт.', show_alert=True
        )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='buy_product:', state="*")
async def buy_product_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = User(call.from_user.id)
    product_id, amount = call.data.split(":")[1], int(call.data.split(":")[2])
    product = await Product().getById(product_id)
    price = float(product[3])
    if price <= float(user.balance):
        products = await Product().get_amount_products(
            product_id=product_id
        )
        if amount <= products:
            await user.updateBalance(-price)
            await user.updatePurchases(
                value=1
            )
            file_name = await Product().get_products(
                product_id=product_id,
                amount=amount
            )
            product = await Product().getById(product_id)
            subcatalog = await SubCatalog().get_subcategory(product[1])
            category = await Catalog().get_category(subcatalog[2].replace('c_', ''))
            file = open(file=file_name, mode='r+')
            await User(call.from_user.id).addPunshare(category[0], product[2], file.read())
            caption = f'''🛒 <b>Заказ</b> #{product[0]}
├<i>Категория: «{category[1]}»</i>
├<i>Под-категория:</i> «<code>{subcatalog[1]}</code>»
├<i>Товар: «{product[2]}»</i>
├<i>В наличии: {products} шт.</i>
├<i>Цена: {price}₽</i>
├<i>Куплено: {amount} шт.</i>
├<i>Статус: ✅ Выполнен</i>
└<i>Описание: {product[4]}</i>

💰 <b>Информация о балансе</b>
├<i>Текущий баланс: {user.balance}</i>
└<i>Crypto баланс: {await user.getBtcBalance()} BTC</i>

🛍️ <b>Ваш товар</b>
└<i>{file.read()}</i>

📄 Руководство по использованию
└<i>Мануал по использованию</i>'''
            await call.message.delete()


            await call.message.answer(text=caption)

            await bot.send_message(
                chat_id=config.config("admin_group"),
                text=f'Куплен товар!\n '
                        f'Пользователь: @{user.username} | {call.from_user.id}\n'
                        f'Товар: {file.read()}'
            )

            with open(file_name, 'r', encoding='UTF-8') as txt:
                for i in txt:
                    await Product().write_history(
                        user_id=call.from_user.id,
                        product_id=product_id,
                        text=i
                    )
            file.close()
            os.remove(file_name)

        else:
            await call.answer(
                text='Товара в таком количестве больше нет!'
            )
    else:
        await call.answer(
            text='❌ У вас недостаточно средств, для покупки данного товара.', show_alert=True
        )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='buy_product_confirm:', state='*')
async def buy_product_confirm(call: types.CallbackQuery, state: FSMContext):
    count = call.data.split(':')[2]
    user = User(call.from_user.id)
    product_id = call.data.split(':')[1]
    info = await Product().get_product(product_id)
    productCount = await Product().get_amount_products(product_id)
    if count.isdigit() is False or (count.isdigit() and productCount < int(count)):
        products = await Product().get_amount_products(
            product_id=product_id
        )
        subcatalog = await SubCatalog().get_subcategory(info[0][1])
        catalog = await Catalog().get_category(subcatalog[2])
        await call.message.edit_caption(
            caption=product.format(
                subcategory=subcatalog[1],
                catalog=catalog[1],
                name=info[0][2],
                price=info[0][3],
                balance=user.balance,
                description=info[0][4],
                amount_product=products,
                btcBalance=await user.getBtcBalance()
            ) + f'\n❌ <b>Вы ввели некорректное число. Еще раз введите, либо выберите желаемое число товара от 1 до {productCount}, на покупку:</b>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await state.finish()
        productCount = await Product().get_amount_products(product_id)
        count = int(count)
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('💰 Купить', callback_data='buy_product:'+product_id+':'+str(count)),
        ).add(
            types.InlineKeyboardButton('❌ Отменить', callback_data='to_catalog')
        ).add(
            types.InlineKeyboardButton('Назад', callback_data='product:'+product_id)
        )
        products = await Product().get_amount_products(
            product_id=product_id
        )
        info = await Product().get_product(product_id)
        productCount = await Product().get_amount_products(info[0][0])
        subcatalog = await SubCatalog().get_subcategory(info[0][1])
        catalog = await Catalog().get_category(subcatalog[2])
        await call.message.edit_caption(
            caption=product.format(
                subcategory=subcatalog[1],
                catalog=catalog[1],
                name=info[0][2],
                price=info[0][3],
                balance=user.balance,
                description=info[0][4],
                amount_product=products,
                btcBalance=await user.getBtcBalance()
            ) + f'\n❓ <b>Вы уверены, что желаете приобрести данный товар в количестве: {count} шт.</b>',
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup
        )




@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='proxy_type:')
async def proxy_type_handler(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption='<b>Выберите время аренды прокси:</b>',
        reply_markup=Proxy().proxy_time_menu(
            proxy_type=call.data.split(":")[1]
        )
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='proxy_time:')
async def proxy_time_handler(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption='<b>Выберите страну аренды прокси:</b>',
        reply_markup=Proxy().proxy_country_menu(
            proxy_type=call.data.split(":")[1],
            proxy_time=call.data.split(":")[2]
        )
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='proxy_country:')
async def proxy_country_handler(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption='<b>Выберите количество проксей для покупки:</b>',
        reply_markup=Proxy().proxy_count_menu(
            proxy_type=call.data.split(":")[1],
            proxy_time=call.data.split(":")[2],
            proxy_country=call.data.split(":")[3]
        )
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='proxy_сount:')
async def proxy_count_handler(call: types.CallbackQuery):
    text, markup = await Proxy().proxy_buy_info(
        proxy_type=call.data.split(":")[1],
        proxy_time=call.data.split(":")[2],
        proxy_country=call.data.split(":")[3],
        proxy_count=call.data.split(":")[4]
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='proxy_buy:')
async def proxy_count_handler(call: types.CallbackQuery):
    msg = await call.message.edit_caption(
        caption='<b>♻️ Подождите...</b>',
        reply_markup=close_markup()
    )
    await Proxy().buy_proxy(
        bot=bot,
        user_id=call.from_user.id,
        proxy_type=call.data.split(":")[1],
        proxy_time=call.data.split(":")[2],
        proxy_country=call.data.split(":")[3],
        proxy_count=call.data.split(":")[4],
        proxy_price=call.data.split(":")[5],
        msg_id=msg.message_id
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='cheat_serivce:')
async def cheat_service_handler(call: types.CallbackQuery):
    markup = await SMMPanel().cheat_type_menu(call.data.split(":")[1])
    await call.message.edit_caption(
        caption='<b> Выберите тип накрутки:</b>',
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='cheat_type:')
async def cheat_type_handler(call: types.CallbackQuery):
    markup = await SMMPanel().cheat_order_menu(
        service=call.data.split(":")[1],
        cheat_type=call.data.split(":")[2]
    )
    await call.message.edit_caption(
        caption='<b> Выберите нужное вам:</b>',
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='cheat_order:')
async def cheat_order_handler(call: types.CallbackQuery):
    text = await SMMPanel().cheat_messages(
        service=call.data.split(":")[1],
        cheat_type=call.data.split(":")[2],
        order=call.data.split(":")[3]
    )
    markup = await SMMPanel().cheat_buy_menu(
        service=call.data.split(":")[1],
        cheat_type=call.data.split(":")[2],
        order=call.data.split(":")[3]
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='cheat_buy_update:')
async def cheat_buy_update_handler(call: types.CallbackQuery):
    service, cheat_type, order, amount, price, update = call.data.split(":")[1], call.data.split(":")[2], \
                                                        call.data.split(":")[3], int(call.data.split(":")[4]), \
                                                        float(call.data.split(":")[5]), int(call.data.split(":")[6])
    orders = SMMPanel().cheat.get(f'{service}').get(cheat_type)
    order_info = orders.get(order)

    if (amount + update) >= int(order_info.get('min')):
        if int(order_info.get('max')) >= amount + update:
            markup = await SMMPanel().cheat_buy_menu(
                service=service,
                cheat_type=cheat_type,
                order=order,
                amount=amount,
                price=price,
                update=update
            )
            await call.message.edit_reply_markup(
                reply_markup=markup)

        else:
            await call.answer(
                text=f'❕ Максимально за раз можно купить {order_info.get("max")}'
            )
    else:
        await call.answer(
            text=f'❕ Минимальное количество для покупки {order_info.get("min")}'
        )
    await call.answer()


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='cheat_buy:')
async def cheat_buy_handler(call: types.CallbackQuery, state: FSMContext):
    service, cheat_type, order, amount, price = call.data.split(":")[1], call.data.split(":")[2], \
                                                call.data.split(":")[3], call.data.split(":")[4], call.data.split(":")[
                                                    5]
    await BuyCheating.link.set()

    async with state.proxy() as data:
        data['service'] = service
        data['type'] = cheat_type
        data['order'] = order
        data['count'] = amount

    await call.message.edit_caption(
        caption=f'<b>📛 Важно!\n '
                f'Вводить правильно ссылку на нужный вам вид услуги! При неправильном вводе - у вас пропадают деньги!</b>',
        reply_markup=close_markup()
    )
    await call.message.answer(
        text="<b>Введите ссылку:</b>"
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='cheat_count:')
async def cheat_count_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    service, cheat_type, order = call.data.split(":")[1], call.data.split(":")[2], call.data.split(":")[3]
    await BuyCheating.count.set()

    async with state.proxy() as data:
        data['service'] = service
        data['type'] = cheat_type
        data['order'] = order

    await call.message.answer(
        text='<b>Введите количество услуги:</b>'
    )

def convertToBtc(amount):
    res = requests.get('https://blockchain.info/ticker').json()
    result = round(float(amount) / res['RUB']['15m'] , 8) 
    return result

@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='return_to_cabinet', state="*")
async def return_to_cabinet_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = User(call.from_user.id)
    
    if user.purchases == 0:
        statusUser = '🥸 Новичок'
    elif user.purchases >= 1 and user.purchases <= 5:
        statusUser = '😎 Постоялец'
    elif user.purchases > 5:
        statusUser = '🤑 Скупщик'
    
    balanceBtc = convertToBtc(user.balance)
    await call.message.edit_caption(
        caption=cabinet_msg.format(
            user_id=call.from_user.id,
            login=call.from_user.username,
            data=user.get_days(),
            balance=user.balance,
            status=statusUser,
            btcBalance=balanceBtc
        ),
        reply_markup=cabinet_markup()
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='referral')
async def referral_handler(call: types.CallbackQuery):
    name = await bot.get_me()
    user = User(call.from_user.id)
    referals = await user.getCountRefferal()
    ref =  await refWithdraws(call.from_user.id).allReferalBalance()
    await call.message.edit_caption(
        caption=refferal.format(
            bot_login=name.username,
            user_id=call.from_user.id,
            referals=referals,
            refBalance=user.refBalance,
            ref=ref
        ),
        reply_markup=refereals_markup()
    )


@vip.callback_query_handler(text='referalls')
async def referalls(call: types.CallbackQuery):
    ref = Referals(call.from_user.id)
    referals = await ref.getRefCount()   
    if referals == 0:
        return await call.answer('❗️ У вас отсутствуют рефералы', show_alert=True)
    last_ref = await ref.getLastReferal()
    firstStepRef = len(await ref.getFirstStepReferals())
    secondStepRef = len(await ref.getSecondStepReferals())
    lastRefString = f"{'@' + last_ref[5]} | {datetime.datetime.strftime('%d.%m.%Y')} в {datetime.datetime.strftime('%H:%M')}" if last_ref is not None else 'Нет'
    await call.message.edit_caption(f'''👬 <b>Рефералы</b>
├<i>Рефералов 1 уровня:</i> <code>{firstStepRef}</code>
├<i>Рефералов 2 уровня:</i> <code>{secondStepRef}</code>
├<i>Активных рефералов:</i> <code>{referals}</code>
└<i>Последний реферал:</i> <code>{lastRefString}</code>''', parse_mode=types.ParseMode.HTML, reply_markup=return_cabinet_markup())


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='withdrawRef')
async def withdrawRef(call: types.CallbackQuery):
    await call.message.edit_caption(caption='''💸 <b>Вывод</b>
└<i>Выберите желаемый вид вывода. Вы можете вывести средства по своим реквизитам, либо же на основной баланс бота.</i>''', parse_mode=types.ParseMode.HTML, reply_markup=withdrawRef_markup())


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='promocode')
async def promocode_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_caption(caption='''🎁 <b>Промокод</b>
└<i>Введите номер Вашего промокода, для его активации.</i>''', parse_mode=types.ParseMode.HTML, reply_markup=return_cabinet_markup()
    )
    await ActivatePromo.promo.set()
    async with state.proxy() as data:
        data['messageid'] = call.message.message_id


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='my_purchases')
async def my_purchases_handler(call: types.CallbackQuery):
    punshareCount = len(await User(call.from_user.id).getPurchases())
    if punshareCount == 0:
        await call.answer('❗️ У вас отсутствуют покупки', show_alert=True)
    else:
        await call.message.edit_caption(
            caption='''🛍️ <b>Мои покупки</b>
└<i>Выберите желаемую категорию:</i>''',
            reply_markup=purchases_markup()
        )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='my_product_order')
async def my_product_order_handler(call: types.CallbackQuery):
    markup = await User(call.from_user.id).purchases_history()
    await call.message.edit_caption(
        caption='Ваши покупки:',
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='my_proxy_order')
async def my_proxy_order_handler(call: types.CallbackQuery):
    markup = await Proxy().user_proxy_menu(
        user_id=call.from_user.id
    )
    if markup is not None:
        await call.message.edit_caption(
            caption='<b>Выберите нужные купленные прокси</b>',
            reply_markup=markup
        )
    else:
        await call.answer(
            text='У вас нет купленных прокси'
        )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='my_proxy_page:')
async def my_proxy_page_handler(call: types.CallbackQuery):
    markup = await Proxy().user_proxy_menu(
        user_id=call.from_user.id,
        page_number=int(call.data.split(":")[1])
    )
    await call.message.edit_caption(
        caption='<b>Выберите нужные купленные прокси</b>',
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='my_proxy_logs:')
async def my_proxy_logs_handler(call: types.CallbackQuery):
    text, markup = await Proxy().user_info_order(
        logs_id=call.data.split(":")[1]
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='my_active_proxy')
async def my_active_proxy_handler(call: types.CallbackQuery):
    markup = await Proxy().user_act_proxy_menu(
        user_id=call.from_user.id
    )
    if markup is not None:
        await call.message.edit_caption(
            caption='<b>Выберите нужные активные прокси</b>',
            reply_markup=markup
        )
    else:
        await call.answer(
            text='У вас нет активных проксей'
        )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='act_proxy_page:')
async def act_proxy_page_handler(call: types.CallbackQuery):
    markup = await Proxy().user_act_proxy_menu(
        user_id=call.from_user.id,
        page_number=int(call.data.split(":")[1])
    )
    await call.message.edit_caption(
        caption='<b>Выберите нужные кулпенные прокси</b>',
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='my_act_proxy:')
async def my_act_proxy_handler(call: types.CallbackQuery):
    text, markup = await Proxy().user_info_act_order(
        logs_id=call.data.split(":")[1]
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='user_purchase:')
async def user_purchase_handler(call: types.CallbackQuery):
    text, markup = await Product().info_purchase_history(
        purchase_id=call.data.split(":")[1]
    )
    await call.message.delete()
    await call.message.answer(
        text=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='renew_proxy:')
async def renew_proxy_handler(call: types.CallbackQuery):
    markup = Proxy().renew_proxy_time(
        order_id=call.data.split(":")[1],
        logs_id=call.data.split(":")[2]
    )
    await call.message.edit_caption(
        caption='<b> Выберите срок продления прокси:</b>',
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='renew_proxy_time:')
async def renew_proxy_time_handler(call: types.CallbackQuery):
    text, markup = await Proxy().renew_proxy_info(
        order_id=call.data.split(":")[1],
        time=call.data.split(":")[2]
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='proxy_renew:')
async def proxy_renew_handler(call: types.CallbackQuery):
    text, markup = await Proxy().proxy_renew_order(
        bot=bot,
        user_id=call.from_user.id,
        order_id=call.data.split(":")[1],
        time=call.data.split(":")[2],
        price=call.data.split(":")[3],
        service_price=call.data.split(":")[4]
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text='my_cheat_order')
async def my_cheat_order_handler(call: types.CallbackQuery):
    markup = await SMMPanel().user_cheatlogs_menu(
        user_id=call.from_user.id
    )
    if markup is not None:
        await call.message.edit_caption(
            caption='<b>Выберите нужные купленные услуги</b>',
            reply_markup=markup
        )
    else:
        await call.answer(
            text='У вас нет купленной накрутки'
        )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='my_cheat_page:')
async def my_cheat_page_handler(call: types.CallbackQuery):
    markup = await SMMPanel().user_cheatlogs_menu(
        user_id=call.from_user.id,
        page_number=int(call.data.split(":")[1])
    )
    await call.message.edit_caption(
        caption='<b>Выберите нужные купленные услуги</b>',
        reply_markup=markup
    )


@vip.callback_query_handler(IsBan(), SubscribeFilter(), text_startswith='my_cheat_logs:')
async def my_cheat_logs_handler(call: types.CallbackQuery):
    text, markup = await SMMPanel().cheat_info_order(
        order_id=call.data.split(":")[1]
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=markup
    )
