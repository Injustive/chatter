from utils.decoder_parser import *
from ui.ui_utils.controller import (invalid_login, register_done, register_failed,
                                    login_done, add_contact_failed, contact_added,
                                    get_contacts_result, get_messages_result, get_message)
from client.client_utils.utils import current_user, current_token


def handle_invalid_login(context):
    invalid_login(context.context_ui)


def handle_login_done(context, data, token):
    current_token.token = token.access_token
    current_user.id = data.id
    current_user.username = data.username
    login_done(context.context_ui)


def handle_register_done(context):
    register_done(context.context_ui)


def handle_register_failed(context, error):
    register_failed(context.context_ui, error)


def handle_add_contact_failed(context, error):
    add_contact_failed(context.context_ui, error)


def handle_contact_added(context):
    contact_added(context.context_ui)


def handle_get_contacts_result(context, contacts):
    get_contacts_result(context.context_ui, contacts)


def handle_get_messages_result(context, messages):
    get_messages_result(context.context_ui, messages)


def handle_get_message(context, message):
    get_message(context.context_ui, message)


def build_login(login, password):
    login = Login(username=login, password=password)
    data = BaseData(command="login", data=login)
    return data


def build_register(user_data):
    user_data = User(**user_data)
    data = BaseData(command="register", data=user_data)
    return data


def build_add_contact(contact):
    contact = UserContact(id=current_user.id, username=current_user.username, contact=contact)
    token = Jwt(access_token=current_token.token)
    data = BaseData(command="add_contact", data=contact, token=token)
    return data


def build_get_contacts():
    user = UserUsername(id=current_user.id, username=current_user.username)
    token = Jwt(access_token=current_token.token)
    data = BaseData(command="get_contacts", data=user, token=token)
    return data


def build_get_messages(contact):
    user = UserContact(id=current_user.id, username=current_user.username, contact=contact.username)
    token = Jwt(access_token=current_token.token)
    data = BaseData(command="get_messages", data=user, token=token)
    return data


def build_send_msg(msg, contact):
    msg = Message(id=current_user.id, username=current_user.username, send_to=contact.username, message=msg)
    token = Jwt(access_token=current_token.token)
    data = BaseData(command="send_msg", data=msg, token=token)
    return data


def handle_login(transport, login, password):
    login_data = build_login(login, password).json()
    print(f"Data send: {login_data}")
    transport.write(login_data.encode())


def handle_register(transport, user_data):
    register_data = build_register(user_data).json()
    print(f"Data send: {register_data}")
    transport.write(register_data.encode())


def handle_add_contact(transport, contact):
    add_contact_data = build_add_contact(contact).json()
    print(f"Data send: {add_contact_data}")
    transport.write(add_contact_data.encode())


def handle_get_contacts(transport):
    get_contacts_data = build_get_contacts().json()
    print(f"Data send: {get_contacts_data}")
    transport.write(get_contacts_data.encode())


def handle_get_messages(transport, contact):
    get_messages_data = build_get_messages(contact).json()
    print(f"Data send: {get_messages_data}")
    transport.write(get_messages_data.encode())


def handle_send_msg(transport, msg, contact):
    send_msg_data = build_send_msg(msg, contact).json()
    print(f"Data send: {send_msg_data}")
    transport.write(send_msg_data.encode())
