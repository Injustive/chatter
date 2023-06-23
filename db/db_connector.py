from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DataAccessLayer:
    """ access to DB fabric"""

    def __init__(self, conn_string, base, echo=False):
        self.engine = None
        self.conn_string = conn_string
        self.echo = echo
        self.Base = base

    async def connect(self):
        self.engine = create_async_engine(self.conn_string, echo=self.echo)
        async with self.engine.begin() as conn:
            # await conn.run_sync(self.Base.metadata.drop_all)
            await conn.run_sync(self.Base.metadata.create_all)

    def create_session(self):
        AsyncSession = async_sessionmaker(self.engine, expire_on_commit=False)
        session = AsyncSession()
        return session
