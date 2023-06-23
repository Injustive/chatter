class ClientTransport:
    def __init__(self, transport=None):
        self.transport = transport


class ContextUi:
    def __init__(self, context_ui=None):
        self.context_ui = context_ui


def invalid_login(context_ui):
    context_ui.invalid_login()


def register_done(context_ui):
    context_ui.register_done()


def register_failed(context_ui, error):
    context_ui.register_failed(error)


def login_done(context_ui):
    context_ui.login_done()


def add_contact_failed(context_ui, error):
    context_ui.add_contact_failed(error)


def contact_added(context_ui):
    context_ui.contact_added()


def get_contacts_result(context_ui, contacts):
    context_ui.get_contacts_result(contacts)


def get_messages_result(context_ui, messages):
    context_ui.get_messages_result(messages)


def get_message(context_ui, message):
    context_ui.get_message(message)


client_transport = ClientTransport()
context = ContextUi()
