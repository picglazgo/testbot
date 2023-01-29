from aiogram.dispatcher.filters.state import State, StatesGroup

class CreateCatalog(StatesGroup):
    name = State()
    confirm = State()

class ChangeCatalog(StatesGroup):
    catalog_id = State()
    name = State()
    confirm = State()

class CreateSubCatalog(StatesGroup):
    category = State()
    name = State()
    confirm = State()

class ChangeSubCatalog(StatesGroup):
    catalog_id = State()
    name = State()
    confirm = State()

class CreateProduct(StatesGroup):
    subcategory_id = State()
    name = State()
    price = State()
    description = State()
    confirm = State()

class ChangeProduct(StatesGroup):
    product_id = State()
    name = State()
    price = State()
    description = State()

class AdminDownloadProduct(StatesGroup):
    product_id = State()
    file = State()
    confirm = State()


class ProductCount(StatesGroup):
    id = State()
    count = State()
    messageid = State()