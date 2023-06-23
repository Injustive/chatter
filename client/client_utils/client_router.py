from client.client_utils.controller import *
from ui.ui_utils.controller import client_transport


class GetRouter:
    def __init__(self, data, token, transport, context):
        self.data = data
        self.token = token
        self.transport = transport
        self.context = context

    def login_done(self):
        handle_login_done(self.context, self.data, self.token)

    def login_failed(self):
        handle_invalid_login(self.context)

    def register_done(self):
        handle_register_done(self.context)

    def register_failed(self):
        handle_register_failed(self.context, error=self.data.error)

    def add_contact_failed(self):
        handle_add_contact_failed(self.context, error=self.data.error)

    def contact_added(self):
        handle_contact_added(self.context)

    def get_contacts_result(self):
        handle_get_contacts_result(self.context, self.data.contacts)

    def get_messages_result(self):
        handle_get_messages_result(self.context, self.data.messages)

    def get_msg(self):
        handle_get_message(self.context, self.data)

    def rout(self, command):
        getattr(self, command)()


class SendRouter:
    def __init__(self, transport):
        self.transport = transport

    def login(self, login, password):
        handle_login(self.transport, login, password)

    def register(self, user_data):
        handle_register(self.transport, user_data)

    def add_contact(self, contact):
        handle_add_contact(self.transport, contact)

    def get_contacts(self):
        handle_get_contacts(self.transport)

    def get_messages(self, contact):
        handle_get_messages(self.transport, contact)

    def send_msg(self, msg, contact):
        handle_send_msg(self.transport, msg, contact)


class RouterMixin:
    def __init__(self):
        self.transport = client_transport.transport
        self._sr = SendRouter(self.transport)

    def login(self, login, password):
        self._sr.login(login, password)

    def register(self, user_data):
        self._sr.register(user_data)

    def add_contact(self, contact):
        self._sr.add_contact(contact)

    def get_contacts(self):
        self._sr.get_contacts()

    def get_messages(self, contact):
        self._sr.get_messages(contact)

    def send_msg(self, msg, contact):
        self._sr.send_msg(msg, contact)
