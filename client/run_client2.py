from client.client_proto import ClientProtocol
from ui.windows import MainWindow
from ui.ui_utils.controller import client_transport, context
from utils.config import SERVER_HOST, SERVER_PORT
import asyncio
from PyQt5 import QtWidgets
import sys
from quamash import QEventLoop


def main():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    message = """{"command": "probe"}"""
    coro = loop.create_connection(lambda: ClientProtocol(context_ui=context),
                                  SERVER_HOST, SERVER_PORT)
    transport, _ = loop.run_until_complete(coro)
    client_transport.transport = transport

    with loop:
        window = MainWindow()
        window.show()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print("Connection closed")


main()
