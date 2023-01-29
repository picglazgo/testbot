from aiosqlite import connect
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
from datetime import datetime
import os

class Catalog():
    def __init__(self):
        self.sql_path = './data/database.db'

    async def get_category(self, category_id):
        category_id = category_id.replace('c_', '')
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM category WHERE id = ?', [category_id])
            self.category = await select.fetchone()
            self.category_id = self.category[0]
            self.category_name = self.category[1]
        
        return self.category_id, self.category_name

    async def get_all_category(self):
        async with connect(self.sql_path) as db:
            info = await db.execute('SELECT * FROM category')
            self.category = await info.fetchall()

        return self.category

    async def delete_catalog(self, category_id):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM category WHERE id = ?', [category_id])
            await db.commit()

    async def update_name(self, category_id, name):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE category SET name = ? WHERE id = ?', [name, category_id])
            await db.commit()

    async def get_menu(self):
        category = list(await self.get_all_category())

        markup = types.InlineKeyboardMarkup(row_width=2)


        x1 = 0
        x2 = 1

        for i in range(len(category)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{category[x1][1]}', callback_data = f'catalog:{category[x1][0]}'),
                    types.InlineKeyboardButton(text = f'{category[x2][1]}', callback_data = f'catalog:{category[x2][0]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{category[x1][1]}', callback_data = f'catalog:{category[x1][0]}'),
                    )
                    break
                except:pass



        return markup

    async def adm_catalog_menu(self):
        category = list(await self.get_all_category())

        markup = types.InlineKeyboardMarkup(row_width=2)


        x1 = 0
        x2 = 1

        for i in range(len(category)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{category[x1][1]}', callback_data = f'adm_catalog:{category[x1][0]}'),
                    types.InlineKeyboardButton(text = f'{category[x2][1]}', callback_data = f'adm_catalog:{category[x2][0]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{category[x1][1]}', callback_data = f'adm_catalog:{category[x1][0]}'),
                    )
                    break
                except:pass

        return markup

    async def create_catalog(self, name):
        async with connect(self.sql_path) as db:
            await db.execute('INSERT INTO category VALUES (?,?)', [f'c_{randint(111, 999)}', name])
            await db.commit()


class SubCatalog():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'

    async def get_subcategory(self, subcategory_id = None):
        async with connect(self.sql_path) as db:
            
            select = await db.execute('SELECT * FROM subcategory WHERE id = ?', [subcategory_id])
            info = await select.fetchone()
            self.subcategory = info

            self.subcategory_id = self.subcategory[0]
            self.category = self.subcategory[1]
            self.subcategory_name = self.subcategory[2]

            return self.subcategory_id, self.subcategory_name, self.category
    
    async def delete_subcatalog(self, subcategory_id):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM subcategory WHERE id = ?', [subcategory_id])
            await db.commit()

    async def get_all_subcategory(self, category_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM subcategory WHERE category = ?', [category_id])
            info = await select.fetchall()
        self.subcategory = list(info)
        return self.subcategory

    async def update_name(self, subcategory_id, name):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE subcategory SET name = ? WHERE id = ?', [name, subcategory_id])
            await db.commit()


    async def get_subcategory_menu(self, category_id):
        if 'c_' not in category_id:
            category_id = 'c_' + category_id

        await self.get_all_subcategory(category_id)
    
        markup = types.InlineKeyboardMarkup(row_width=2)

        x1 = 0
        x2 = 1

        for i in range(len(self.subcategory)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{self.subcategory[x1][2]}', callback_data = f'subcatalog:{self.subcategory[x1][0]}'),
                    types.InlineKeyboardButton(text = f'{self.subcategory[x2][2]}', callback_data = f'subcatalog:{self.subcategory[x2][0]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{self.subcategory[x1][2]}', callback_data = f'subcatalog:{self.subcategory[x1][0]}'),
                    )
                    break
                except:pass

        markup.add(
                types.InlineKeyboardButton(text = 'Назад', callback_data = 'to_catalog'),
        )

        return markup

    async def adm_subcatalog_menu(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM subcategory')
            info = await select.fetchall()
        self.subcategory = list(info)

        markup = types.InlineKeyboardMarkup(row_width=2)


        x1 = 0
        x2 = 1

        for i in range(len(self.subcategory)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{self.subcategory[x1][2]}', callback_data = f'adm_subcatalog:{self.subcategory[x1][0]}'),
                    types.InlineKeyboardButton(text = f'{self.subcategory[x2][2]}', callback_data = f'adm_subcatalog:{self.subcategory[x2][0]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{self.subcategory[x1][2]}', callback_data = f'adm_subcatalog:{self.subcategory[x1][0]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text = '💢 Закрыть', callback_data = 'to_close')
        )
        return markup
    
    async def create_subcatalog(self, category_id, name):
        async with connect(self.sql_path) as db:
            await db.execute('INSERT INTO subcategory VALUES (?,?,?)', 
                        [f'sub_{randint(111, 999)}', category_id, name])
            await db.commit()

class Product():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'

    async def get_product(self, product_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM product WHERE id = ?', [product_id])
            info = await select.fetchone()

        self.product = info
        self.product_id = self.product[0]
        self.subcategory = self.product[1]
        self.product_name = self.product[2]
        self.product_price = self.product[3]
        self.description = self.product[4]

        return self.product, self.subcategory, self.product_name, self.product_price, self.description


    async def getById(self, id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM product WHERE id = ? LIMIT 1', [id])
            info = await select.fetchone()
        
        return info
    

    async def getByName(self, name):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM product WHERE name = ?', [name])
            info = await select.fetchall()
        
        return list(info)

    async def get_all_product(self, subcategory_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM product WHERE subcategory_id = ?', [subcategory_id])
            info = await select.fetchall()
        self.product = list(info)
        return self.product

    async def get_amount_products(self, product_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM active_product WHERE product_id = ?', [product_id])
            products = await select.fetchall()
        self.amount_products = len(list(products))

        return self.amount_products

    async def create_product(self, subcategory_id, name, price, description):
        async with connect(self.sql_path) as db:
            product = [f'p_{randint(1111, 9999)}', subcategory_id, name, price, description]
            await db.execute('INSERT INTO product VALUES (?,?,?,?,?)', product)
            await db.commit()

    async def delete_product(self, product_id):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM product WHERE id = ?', [product_id])
            await db.commit()

    async def get_products(self, product_id, amount): 
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM active_product WHERE product_id = ?', [product_id])
            lists  = await select.fetchmany(int(amount))
        
        id_lists = await self.get_id_list(lists)
        await self.del_products(product_id, id_lists)
        file_name = f'./utils/docs/product_{randint(1111, 9999)}.txt'

        with open(file_name, 'w+', encoding='UTF-8') as txt:
            for i in lists:
                txt.write(i[3])
            
        return file_name

    async def get_id_list(self, products_list):
        id_list = []

        for i in products_list:
            id_list.append(i[0])

        return id_list

    async def del_products(self, product_id, id_list):
        async with connect(self.sql_path) as db:

            for i in id_list:
                await db.execute('DELETE FROM active_product WHERE id = ?', [i])
                await db.commit()

    async def upload_product(self, product_id, file_name):
        name = await self.get_product(product_id)

        n = '\n'
        good = 0
        bad = 0
        with open(file_name, 'rb') as txt:
            for i in txt.readlines():
                i = i.decode(errors='ignore').replace(n, "")
                try:
                    async with connect(self.sql_path) as db:
                        sql = f'INSERT INTO active_product VALUES (?,?,?,?)'
                        product = [randint(111, 9999), product_id, name[2], i]
                        await db.execute('INSERT INTO active_product VALUES (?,?,?,?)', product)
                        await db.commit()

                    good += 1
                except Exception as e:
                    bad += 1
        os.remove(file_name)

        return good, bad

    async def write_history(self, user_id, product_id, text):
        name = await self.get_product(product_id)
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT COUNT(*) FROM purchase_history')
            count = await select.fetchone()
            tovar = [count[0] + 1, user_id, product_id, f'{name[2]}', text, datetime.now()]
            await db.execute('INSERT INTO purchase_history VALUES (?,?,?,?,?,?)', tovar)
            await db.commit()

    async def update_name(self, product_id, name):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE product SET name = ? WHERE id = ?', [name, product_id])
            await db.commit()

    async def update_price(self, product_id, price):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE product SET price = ? WHERE id = ?', [price, product_id])
            await db.commit()

    async def update_description(self, product_id, description):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE product SET description = ? WHERE id = ?', [description, product_id])
            await db.commit()

    async def get_product_menu(self, subcategory_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM product WHERE subcategory_id = ?', [subcategory_id])
            info = await select.fetchall()
        self.product = list(info)
        markup = types.InlineKeyboardMarkup(row_width=2)

        subcategory = await SubCatalog().get_subcategory(info[0][1])
        x1 = 0
        x2 = 1

        for i in range(len(self.product)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{self.product[x1][2]}', callback_data = f'product:{self.product[x1][0]}'),
                    types.InlineKeyboardButton(text = f'{self.product[x2][2]}', callback_data = f'product:{self.product[x2][0]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{self.product[x1][2]}', callback_data = f'product:{self.product[x1][0]}'),
                    )
                    break
                except:pass

        markup.add(
                types.InlineKeyboardButton(text = 'Назад', callback_data = 'catalog:'+subcategory[2]),
        )

        return markup

    @staticmethod
    async def buy_product_markup(product_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text = '💰 Купить', callback_data = f'product_buy:{product_id}'),
            types.InlineKeyboardButton(text = 'Назад', callback_data = 'to_catalog'),
        )

        return markup

    async def get_buy_menu(self, product_id, productCount, amount=None, price=None, update=None):

        if amount == None and price == None:
            info = await self.get_product(product_id)

            amount = 1
            price = info[3]
        elif update != None:
            info = await self.get_product(product_id)

            amount += update
            price = float(info[3]) * amount

        markup = InlineKeyboardMarkup()

        if productCount != 1:
            markup.add(
                InlineKeyboardButton(text='⬇️', callback_data=f'buy_menu_update:{product_id}:{amount}:{price}:-1'),
                InlineKeyboardButton(text=f'{amount} шт', callback_data='amount_product'),
                InlineKeyboardButton(text='⬆️', callback_data=f'buy_menu_update:{product_id}:{amount}:{price}:1')
            )
        if productCount >= 10:
            markup.add(
                InlineKeyboardButton(text='- 10', callback_data=f'buy_menu_update:{product_id}:{amount}:{price}:-10'),
                InlineKeyboardButton(text='+ 10', callback_data=f'buy_menu_update:{product_id}:{amount}:{price}:10'),
            )

        markup.add(
            InlineKeyboardButton(text=f'💰 Купить за {price} руб', callback_data=f'buy_product_confirm:{product_id}:{amount}:{price}')
        ).add(
            InlineKeyboardButton(text='Назад', callback_data=f'product:{product_id}'),
        )

        return markup 

    async def adm_product_menu(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM product')
            info = await select.fetchall()
        self.product = list(info)

        markup = types.InlineKeyboardMarkup(row_width=2)


        x1 = 0
        x2 = 1

        for i in range(len(self.product)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{self.product[x1][2]}', callback_data = f'adm_product:{self.product[x1][0]}'),
                    types.InlineKeyboardButton(text = f'{self.product[x2][2]}', callback_data = f'adm_product:{self.product[x2][0]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{self.product[x1][2]}', callback_data = f'adm_product:{self.product[x1][0]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text = '💢 Закрыть', callback_data = 'to_close')
        )
        return markup

    async def info_purchase_history(self, purchase_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM purchase_history WHERE id = ?', [purchase_id])
            info = await select.fetchone()

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add( 
                types.InlineKeyboardButton(text='💢 Закрыть', callback_data='to_close'),
            )

        msg = f"""
<b>🖲 Название:</b> {info[3]}

<b>🔗 Дата покупки:</b> {info[5][:10]}

<b>♻️ Товар:</b> 
<code>{info[4]}</code>

        """

        return msg, markup


class notificationProduct():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'


    async def getAllUsersByName(self, product_name = None):
        async with connect(self.sql_path) as db:
            product = await Product().getByName(product_name)
            res =  await db.execute("SELECT * FROM notificationProduct WHERE product_id = ?", [product[0][0]])
            res = await res.fetchall()
            return res


    async def deleteRowByName(self, product_name, user_id):
        async with connect(self.sql_path) as db:
            product = await Product().getByName(product_name)
            await db.execute("DELETE FROM notificationProduct WHERE product_id = ? AND user_id=?", [product[0][0], user_id])
            await db.commit()

    
    async def createNotifiction(self, product_name, user_id):
        async with connect(self.sql_path) as db:
            product = await Product().getByName(product_name)
            await db.execute("INSERT INTO notificationProduct VALUES (?, ?)", [product[0][0], user_id])
            await db.commit()

    
    async def haveBind(self, product_name, user_id):
        async with connect(self.sql_path) as db:
            product = await Product().getByName(product_name)
            res = await db.execute("SELECT * FROM notificationProduct WHERE product_id=? AND user_id=?", [product[0][0], user_id])
            return True if await res.fetchone() is not None else False