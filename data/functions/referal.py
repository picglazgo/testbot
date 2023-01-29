
from . import AioSQL


class Referals(AioSQL):
    def __init__(self,
                 user_id: str = None) -> None:
        super().__init__()

        if user_id is not None:
            self.user_id: int = user_id


    async def getFirstStepReferals(self):
        await self.__ainit__()
        await self.db.execute("SELECT * FROM referals WHERE refer_id=?", [self.user_id])
        return await self.db.fetchall()


    async def getLastStepReferals(self):
        await self.__ainit__()
        await self.db.execute("SELECT * FROM referals WHERE refer_id=? ORDER BY id DESK LIMIT 1", [self.user_id])
        return await self.db.fetchone()


    async def getSecondStepReferals(self):
        await self.__ainit__()
        await self.db.execute("SELECT * FROM referals WHERE owner_refer=?", [self.user_id])
        return await self.db.fetchall()


    async def getLastReferal(self):
        await self.__ainit__()
        await self.db.execute("SELECT * FROM referals WHERE owner_refer=? ORDER BY id DESC LIMIT 1", [self.user_id])
        return await self.db.fetchone()


    async def getRefCount(self):
        await self.__ainit__()
        await self.db.execute("SELECT * FROM referals WHERE owner_refer=?", [self.user_id])
        return len(await self.db.fetchall())