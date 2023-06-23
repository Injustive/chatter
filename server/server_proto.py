from asyncio import Protocol
from utils.decoder_parser import BaseParser
from server.server_utils.server_router import Router
from db.controller import DB
import asyncio


class ServerProtocol(Protocol):
    def __init__(self, connections, users):
        super(ServerProtocol, self).__init__()
        self.connections = connections
        self.users = users
        self.transport = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.connections[transport] = {
            'peername': peername,
            'transport': transport,
            'username': None
        }
        print('Connection from {}'.format(peername))
        self.transport = transport

    def eof_received(self):
        """EOF(end-of-file)"""
        self.transport.close()

    def connection_lost(self, exc):
        """Transport Error , which means the client is disconnected."""
        rm_con = []
        for con in self.connections:
            if con._closing:
                rm_con.append(con)
        for i in rm_con:
            del self.connections[i]

        rm_user = []
        for k, v in self.users.items():
            for con in rm_con:
                if v['transport'] == con:
                    rm_user.append(k)

        for username in rm_user:
            asyncio.create_task(DB.set_online_status(username, False))
            del self.users[username]
            print('{} disconnected'.format(username))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        parser = BaseParser(data)
        command, data, token = parser.command, parser.data, parser.token
        router = Router(data, token, self.transport, self.connections, self.users)
        router.rout(command)
