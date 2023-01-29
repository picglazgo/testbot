
from . import AioSQL


class Promocode(AioSQL):
    def __init__(self,
                 promo: str = None) -> None:
        super().__init__()

        if promo is not None:
            self.promocode: str = promo

    async def getPromoList(self) -> list:
        """
        Получаем список промокодов
        return promocode: list
        """
        await self.__ainit__()
        select = await self.db.execute(
            'SELECT * FROM promocode WHERE name = ?', [self.promocode]
        )
        promocode = await select.fetchone()

        return promocode

    async def getActivatePromo(self,
                               user_id: int) -> None:
        await self.__ainit__()
        info = await self.getPromoList()
        users = f"{info[4]}{user_id},"

        await self.db.execute(
            'UPDATE promocode SET activation = activation - 1, users = ? WHERE name = ?',
            [users, self.promocode]
        )
        await self.conn.commit()

    async def deletePromo(self):
        await self.__ainit__()
        await self.db.execute(
            'DELETE FROM promocode WHERE name = ?', [self.promocode])

        await self.conn.commit()
