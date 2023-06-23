import asyncio
from server.server_proto import ServerProtocol
from utils.config import *
from db.controller import DB


async def main():
    SEPARATOR = "-" * 10
    connections = dict()
    users = dict()

    loop = asyncio.get_running_loop()
    print("{0}Starting server on {1}:{2}{0}".format(SEPARATOR, SERVER_HOST, SERVER_PORT))
    server = await loop.create_server(lambda: ServerProtocol(connections, users), SERVER_HOST, SERVER_PORT)
    print("{0}Server started, address-{1}{0}".format(SEPARATOR, server.sockets[0].getsockname()))

    print("{0}Starting database{0}".format(SEPARATOR))
    await DB.connect_db()
    print("{0}Database started{0}".format(SEPARATOR))

    async with server:
        await server.serve_forever()

asyncio.run(main())
