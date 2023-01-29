# © copyright by VoX DoX
from aiosqlite import connect


class AioSQL:
    def __init__(self):
        self._SQL_PATH_ = "./data/database.db"

    async def __ainit__(self):
        self.conn = await connect(self._SQL_PATH_)
        self.db = await self.conn.cursor()
