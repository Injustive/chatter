import asyncio
from utils.decoder_parser import BaseParser
from client.client_utils.client_router import GetRouter


class ClientProtocol(asyncio.Protocol):
    def __init__(self, context_ui):
        self.context_ui = context_ui
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        parser = BaseParser(data)
        command, data, token = parser.command, parser.data, parser.token
        router = GetRouter(data, token, self.transport, self.context_ui)
        router.rout(command)

    def connection_lost(self, exc):
        print('The server closed the connection')