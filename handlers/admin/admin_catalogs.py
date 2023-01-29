from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import vip, bot
from keyboards import inline as menu
from states import CreateCatalog, CreateSubCatalog, ChangeCatalog, ChangeSubCatalog
from utils import Catalog, SubCatalog


@vip.callback_query_handler(text='adm_act_catalog')
async def adm_catalog_act(call: types.CallbackQuery):
    markup = await Catalog().adm_catalog_menu()
    await call.message.edit_text(text='Выберите каталог:', reply_markup=markup)


@vip.callback_query_handler(text_startswith='adm_catalog:')
async def admin_info_catalog(call: types.CallbackQuery):
    name = await Catalog().get_category(call.data.split(":")[1])
    await call.message.edit_text(text=f'Каталог: {name[1]}', reply_markup=menu.adm_catalog_info(call.data.split(":")[1]))


@vip.callback_query_handler(text_startswith='delete_catalog:')
async def adm_delete_catalog(call: types.CallbackQuery):
    await Catalog().delete_catalog(call.data.split(":")[1])
    await call.message.edit_text('Каталог успешно удален!', reply_markup=menu.close_markup())


@vip.callback_query_handler(text_startswith='edit_name_catalog:')
async def admin_edit_catalog(call: types.CallbackQuery, state: FSMContext):
    name = await Catalog().get_category(call.data.split(":")[1])
    await ChangeCatalog.name.set()
    async with state.proxy() as data:
        data['catalog_id'] = call.data.split(":")[1]
    await call.message.edit_text(text=f'Введите новое название для каталога: {name[1]}')


@vip.message_handler(state=ChangeCatalog.name)
async def admin_change_catalog(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await msg.answer(f'Изменение названия каталога на {msg.text}\nПодтвердить "+"')
    await ChangeCatalog.next()


@vip.message_handler(state=ChangeCatalog.confirm)
async def admin_change_catalog_2(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            catalog_id = data['catalog_id']
            name = data['name']
        await Catalog().update_name(catalog_id, name)
        await msg.answer('Название каталога успешно изменено!')
    else:
        await msg.answer('Изменение названия отменено!')
    await state.finish()


@vip.callback_query_handler(text='adm_create_catalog')
async def adm_catalog_create(call: types.CallbackQuery):
    await CreateCatalog.name.set()
    await call.message.answer('Введите название нового каталога')


@vip.message_handler(state=CreateCatalog.name)
async def adm_catalog_create_2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await msg.answer(f'Введите "+", для создания каталога: {msg.text}')
    await CreateCatalog.next()


@vip.message_handler(state=CreateCatalog.confirm)
async def adm_catalog_confirm(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            name = data['name']
        await Catalog().create_catalog(name)
        await msg.answer(f'Каталог: {name} успешно создан!')
    else:
        await msg.answer('Создание каталога отменено!')
    await state.finish()


@vip.callback_query_handler(text='adm_create_subcatalog')
async def adm_subcatalog_create(call: types.CallbackQuery):
    await CreateSubCatalog.category.set()
    markup = await Catalog().adm_catalog_menu()
    await call.message.answer('Выберите категорию, в которой нужно создать подкаталог:', reply_markup=markup)


@vip.callback_query_handler(text_startswith='create_subcatalog:')
async def adm_create_subcatalog(call: types.CallbackQuery, state: FSMContext):
    await CreateSubCatalog.name.set()
    async with state.proxy() as data:
        data['category'] = call.data.split(":")[1]
    await call.message.edit_text('Введите название подкаталога:')


@vip.callback_query_handler(state=CreateSubCatalog.category)
async def adm_create_subcatalog_2(call: types.CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data['category'] = category_id
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Введите название подкаталога:')
    await CreateSubCatalog.next()


@vip.callback_query_handler(state=CreateSubCatalog.category)
async def adm_create_subcatalog_2(call: types.CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data['category'] = category_id
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Введите название подкаталога:')
    await CreateSubCatalog.next()


@vip.message_handler(state=CreateSubCatalog.name)
async def adm_subcatalog_create_3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await msg.answer(f'Для создания подкаталога введите "+"')
    await CreateSubCatalog.next()


@vip.message_handler(state=CreateSubCatalog.confirm)
async def adm_subcatalog_create_4(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            category_id = data['category']
            name = data['name']
        await SubCatalog().create_subcatalog(category_id, name)
        await msg.answer(f'Подкаталог: {name} успешно создан!')
    else:
        await msg.answer('Создание подкаталога отменено', reply_markup=menu.close_markup())
    await state.finish()


@vip.callback_query_handler(text='adm_act_subcatalog')
async def active_subcatalog(call: types.CallbackQuery):
    markup = await SubCatalog().adm_subcatalog_menu()
    await call.message.edit_text(text='Выберите подкаталог:', reply_markup=markup)


@vip.callback_query_handler(text_startswith='delete_subcatalog:')
async def adm_delete_subcatalog(call: types.CallbackQuery):
    await SubCatalog().delete_subcatalog(call.data.split(":")[1])
    await call.message.edit_text(text='Подкаталог удален!', reply_markup=menu.close_markup())


@vip.callback_query_handler(text_startswith='adm_subcatalog:')
async def adm_subcatalog(call: types.CallbackQuery):
    name = await SubCatalog().get_subcategory(call.data.split(":")[1])
    markup = menu.adm_subcatalog_info(call.data.split(":")[1])
    await call.message.edit_text(text=f'Подкаталог: {name[1]}\nЧто хотите сделать?', reply_markup=markup)


@vip.callback_query_handler(text_startswith='edit_name_subcatalog:')
async def admin_edit_catalog(call: types.CallbackQuery, state: FSMContext):
    name = await SubCatalog().get_subcategory(call.data.split(":")[1])
    await ChangeSubCatalog.name.set()
    async with state.proxy() as data:
        data['catalog_id'] = call.data.split(":")[1]
    await call.message.edit_text(text=f'Введите новое название для подкаталога: {name[1]}')


@vip.message_handler(state=ChangeSubCatalog.name)
async def admin_change_catalog(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await msg.answer(f'Изменение названия подкаталога на {msg.text}\nПодтвердить "+"')
    await ChangeSubCatalog.next()


@vip.message_handler(state=ChangeSubCatalog.confirm)
async def admin_change_catalog_2(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            catalog_id = data['catalog_id']
            name = data['name']

        await SubCatalog().update_name(catalog_id, name)
        await msg.answer('Название подкаталога успешно изменено!')
    else:
        await msg.answer('Изменение названия отменено!')
    await state.finish()
