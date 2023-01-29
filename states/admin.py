from aiogram.dispatcher.filters.state import State, StatesGroup

class AdmSearch(StatesGroup):
    user_id = State()

class AdminGiveBalance(StatesGroup):
    user_id = State()
    amount = State()
    confirm = State()

class EmailText(StatesGroup):
    text = State()
    action = State()
    down = State()
    down_confirm = State()


class EmailPhoto(StatesGroup):
    photo = State()
    text = State()
    action = State()
    down = State()
    down_confirm = State()

class ButtonsAdd(StatesGroup):
    name = State()
    text = State()
    photo = State()
    confirm = State()

class CreatePromo(StatesGroup):
    name = State()
    money = State()
    amount = State()

class ProxyLineAPIAdd(StatesGroup):
    api = State()
    confirm = State()

class ProxyPercent(StatesGroup):
    percent = State()
    confirm = State()
