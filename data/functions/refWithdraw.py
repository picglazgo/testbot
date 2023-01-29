
from . import AioSQL


class refWithdraws(AioSQL):
    def __init__(self,
                 user_id: str = None) -> None:
        super().__init__()

        if user_id is not None:
            self.user_id: str = user_id


    async def allReferalBalance(self):
        await self.__ainit__()
        await self.db.execute('select * from refWithdraws where user_id=?', [self.user_id])
        items = await self.db.fetchall()
        amount = 0
        for item in items:
            amount += item[2]
        return amount