from server.server_utils.controller import *
from functools import partial


class Router:
    def __init__(self, data, token, transport, connections, users):
        self.data = data
        self.username = data.username if data else None
        self.token = token
        self.transport = transport
        self.connections = connections
        self.users = users

    def probe(self):
        handle_probe(self.transport)

    def login(self):
        task = asyncio.create_task(DB.get_user_by_username(self.username))
        task.add_done_callback(partial(
            handle_login,
            self.username,
            self.data.password,
            self.transport,
            self.users,
            self.connections
            )
        )

    def register(self):
        task = asyncio.create_task(DB.register_user(self.data))
        task.add_done_callback(partial(
            handle_register,
            self.transport))

    def add_contact(self):
        task = asyncio.create_task(DB.add_contact(self.data.id, self.data.contact))
        task.add_done_callback(partial(
            handle_add_contact,
            self.data.id,
            self.username,
            self.transport))

    def send_msg(self):
        msg = self.data.message
        time = self.data.send_time
        send_to = self.data.send_to
        asyncio.create_task(DB.write_msg(
            self.data.id,
            send_to,
            msg,
            time
        ))
        user_send_to = self.users.get(send_to, self.data.send_to)
        handle_send_msg(
            self.data.id,
            self.username,
            self.transport,
            user_send_to,
            msg,
            time)

    def get_contacts(self):
        task = asyncio.create_task(DB.get_contacts(self.data.id))
        task.add_done_callback(partial(handle_get_contacts, self.transport))

    def get_messages(self):
        task = asyncio.create_task(DB.get_all_messages(self.data.id, self.data.contact))
        task.add_done_callback(partial(handle_get_messages, self.transport))

    def rout(self, command):
        auth_required = ["add_contact", "send_msg", "get_contacts", "get_messages"]
        if command not in auth_required:
            getattr(self, command)()
        else:
            @is_authenticated(self.token, self.data.id, self.username, self.transport)
            def run_routing(*args, **kwargs):
                getattr(self, command)()
            run_routing()

