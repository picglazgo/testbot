from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

from loader import vip, bot
from data import adm_product
from keyboards import inline as menu
from utils import Product, SubCatalog
from states import CreateProduct, ChangeProduct, AdminDownloadProduct
from utils.market import Catalog, notificationProduct


@vip.callback_query_handler(text='adm_act_product')
async def admin_product_act(call: types.CallbackQuery):
    await call.message.answer(
        text='Активные товары',
        reply_markup=await Product().adm_product_menu()
    )


@vip.callback_query_handler(text_startswith='adm_product:')
async def adm_products(call: types.CallbackQuery):
    product_id = call.data.split(":")[1]
    info = await Product().get_product(product_id)
    subcatalog = await SubCatalog().get_subcategory(info[0][1])
    catalog = await Catalog().get_category(subcatalog[2])
    text = adm_product.format(catalog=catalog[1],
        name=info[2], price=info[3], 
                        description=info[4], amount_product=await Product().get_amount_products(product_id))
    await call.message.edit_text(text=text, reply_markup=menu.adm_product_info(product_id))


@vip.callback_query_handler(text_startswith='delete_product:')
async def adm_delete_product(call: types.CallbackQuery):
    await Product().delete_product(call.data.split(":")[1])
    await call.message.edit_text("Успешно удален товар!", reply_markup=menu.close_markup())


@vip.callback_query_handler(text='adm_create_product')
async def adm_create_product(call: types.CallbackQuery):
    await CreateProduct.subcategory_id.set()
    markup = await SubCatalog().adm_subcatalog_menu()
    await call.message.answer('Выберите подкаталог, в котором создать товар', reply_markup=markup)


@vip.callback_query_handler(state=CreateProduct.subcategory_id)
async def adm_product_create(call: types.CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data['subcategory_id'] = category_id
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Введите название товара:')
    await CreateProduct.next()


@vip.message_handler(state=CreateProduct.name)
async def adm_product_create_2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await msg.answer('Введите прайс на товар за 1шт')
    await CreateProduct.next()


@vip.message_handler(state=CreateProduct.price)
async def adm_product_create_3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = msg.text
    await msg.answer('Введите описание к товару:')
    await CreateProduct.next()


@vip.message_handler(state=CreateProduct.description)
async def adm_product_create_4(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = msg.text
    await msg.answer('Для создания товара отправьте "+"')
    await CreateProduct.next()



@vip.message_handler(state=CreateProduct.confirm)
async def adm_product_confirm(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            subcatalog = data['subcategory_id']
            name = data['name']
            price = data['price']
            description = data['description']
        users = await notificationProduct().getAllUsersByName(name)
        product = await Product().getByName(name)
        subcatalog = await SubCatalog().get_subcategory(subcatalog[2])
        catalog = await Catalog().get_category(subcatalog[1])

        await Product().create_product(subcatalog, name, price, description)

        await msg.answer(f'Товар {name} успешно создан', reply_markup=menu.close_markup())

    else:
        await msg.answer('Создание товара отменено!', reply_markup=menu.close_markup())
    await state.finish()


@vip.callback_query_handler(text_startswith='edit_name_product:')
async def edit_name_product(call: types.CallbackQuery, state: FSMContext):
    info = await Product().get_product(call.data.split(":")[1])
    await ChangeProduct.name.set()
    async with state.proxy() as data:
        data['product_id'] = call.data.split(":")[1]
    await call.message.answer(f'Введите новое название товара: {info[2]} (для отмены введите "-")')


@vip.message_handler(state=ChangeProduct.name)
async def new_name_product(msg: types.Message, state: FSMContext):
    if not msg.text.startswith("-"):
        async with state.proxy() as data:
            product_id = data['product_id']
        await Product().update_name(product_id, msg.text)
        await msg.answer(f'Успешно обновлено новое название товара: {msg.text}', reply_markup=menu.close_markup())
    else:
        await msg.answer('Изменение названия отменено!', reply_markup=menu.close_markup())
    await state.finish()


@vip.callback_query_handler(text_startswith='edit_price_product:')
async def edit_name_product(call: types.CallbackQuery, state: FSMContext):
    info = await Product().get_product(call.data.split(":")[1])
    await ChangeProduct.price.set()
    async with state.proxy() as data:
        data['product_id'] = call.data.split(":")[1]
    await call.message.answer(f'Введите новую цену товара: {info[2]}  (для отмены введите "-")')


@vip.message_handler(state=ChangeProduct.price)
async def new_name_product(msg: types.Message, state: FSMContext):
    if not msg.text.startswith("-"):
        async with state.proxy() as data:
            product_id = data['product_id']
        info = await Product().get_product(product_id)
        await Product().update_price(product_id, msg.text)
        await msg.answer(f'Успешно обновлена цена товара: {info[2]}, ценник: {msg.text} руб/шт', reply_markup=menu.close_markup())
    else:
        await msg.answer('Изменение цены отменено!', reply_markup=menu.close_markup())
    await state.finish()


@vip.callback_query_handler(text_startswith='edit_descr_product:')
async def edit_name_product(call: types.CallbackQuery, state: FSMContext):
    info = await Product().get_product(call.data.split(":")[1])
    await ChangeProduct.description.set()
    async with state.proxy() as data:
        data['product_id'] = call.data.split(":")[1]
    await call.message.answer(f'Введите новое описание товара: {info[2]}  (для отмены введите "-")')


@vip.message_handler(state=ChangeProduct.description)
async def new_name_product(msg: types.Message, state: FSMContext):
    if not msg.text.startswith("-"):
        async with state.proxy() as data:
            product_id = data['product_id']
        info = await Product().get_product(product_id)
        await Product().update_description(product_id, msg.text)
        await msg.answer(f'Успешно обновлено описание товара: {info[2]}, описание:\n {msg.text}', reply_markup=menu.close_markup())
    else:
        await msg.answer('Изменение описания отменено!', reply_markup=menu.close_markup())
    await state.finish()


@vip.message_handler(state=AdminDownloadProduct.file, content_types=['document'])
async def admin_download_product(msg: types.Message, state: FSMContext):
    file = f'utils/docs/down_{randint(111, 999)}.txt'
    await msg.document.download(destination_file=file)
    async with state.proxy() as data:
        data['file'] = file

    await msg.answer('Для подтверждения загрузки, отправь +')
    await AdminDownloadProduct.next()


# Загрузка товара
@vip.message_handler(state=AdminDownloadProduct.confirm)
async def admin_download_product_2(msg: types.Message, state: FSMContext):
    if msg.text == '+':
        async with state.proxy() as data:
            product_id = data['product_id']
            file = data['file']



        info = await Product().upload_product(product_id, file)
        await msg.answer(f'Загружено: {info[0]}\n Ошибок: {info[1]}')
        await state.finish()

        product = await Product().getById(product_id)
        productCount = await Product().get_amount_products(product_id)
        users = await notificationProduct().getAllUsersByName(product[2])
        subcatalog = await SubCatalog().get_subcategory(product[1])
        catalog = await Catalog().get_category(subcatalog[2])
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('🔍 К товару', callback_data='product:'+product[0]+':notCaption:deleteBack')
        ).add(
            types.InlineKeyboardButton('Понятно', callback_data='deleteMessage')
        )
        for item in users:
            try:
                await msg.bot.send_message(item[1], f'''
📨 <b>Оповещения о наличии</b>
├<i>Категория:</i> «<code>{catalog[1]}</code>»
├<i>Под-категория:</i> «<code>{subcatalog[1]}</code>»
├<i>Товар:</i> «<code>{product[2]}</code>»
└<i>В наличии:</i> <code>{productCount} шт.</code>''', reply_markup=markup)
                await notificationProduct().deleteRowByName(product[2], item[1])
            except:
                pass
    else:
        await state.finish()
        await msg.answer('Отменено!')
