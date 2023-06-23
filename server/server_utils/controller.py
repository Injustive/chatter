import asyncio

from utils.utils import Token
from utils.decoder_parser import *
from db.controller import DB
from jwt import ExpiredSignatureError, InvalidSignatureError
from functools import wraps, partial


def build_send_token(command, access, username, user_id):
    username = UserUsername(id=user_id, username=username)
    token = Jwt(access_token=access)
    data = BaseData(command=command, data=username, token=token)
    return data


def build_bad_jwt_answer():
    data = BaseData(command="bad_token_auth")
    return data


def build_contact_added(username, user_id):
    username = UserUsername(id=user_id, username=username)
    data = BaseData(command="contact_added", data=username)
    return data


def build_bad_login():
    data = BaseData(command="login_failed")
    return data


def build_get_contacts_result(contacts):
    contacts = [Contact.from_orm(contact) for contact in contacts]
    contacts = ContactsList(contacts=contacts)
    data = BaseData(command="get_contacts_result", data=contacts)
    return data


def build_get_messages(messages):
    messages = [Msg(time=message.time,
                    user=message.user,
                    contact=message.contact,
                    message=message.message) for message in messages]
    messages = MessagesList(messages=messages)
    data = BaseData(command="get_messages_result", data=messages)
    return data


def build_register_done():
    data = BaseData(command="register_done")
    return data


def build_register_error(error):
    error_data = Error(error=str(error))
    data = BaseData(command="register_failed", data=error_data)
    return data


def build_add_contact_error(error):
    error_data = Error(error=str(error))
    data = BaseData(command="add_contact_failed", data=error_data)
    return data


def handle_register(transport, done_task):
    error = done_task.exception()
    if not error:
        register_done_data = build_register_done().json().encode()
        transport.write(register_done_data)
    else:
        register_failed_data = build_register_error(error).json().encode()
        transport.write(register_failed_data)


def handle_expired_token(user_id, username, transport, func, done_task, *args, **kwargs):
    jwt = done_task.result()
    bad_jwt_data = build_bad_jwt_answer().json().encode()
    if not jwt:
        transport.write(bad_jwt_data)
        return
    token = Token(token=jwt.token)
    try:
        token.verify()
        access, refresh = Token().access_refresh_tokens
        update_token_data = build_send_token(
            "update_token",
            access,
            username,
            user_id
        ).json().encode()
        task = asyncio.create_task(DB.update_or_create_jwt(user_id, refresh))
        task.add_done_callback(partial(func,
                                       *args,
                                       **kwargs))
        transport.write(update_token_data)
    except (ExpiredSignatureError, InvalidSignatureError):
        asyncio.create_task(DB.delete_jwt(user_id))
        transport.write(bad_jwt_data)


def handle_bad_token(transport):
    bad_jwt_data = build_bad_jwt_answer().json().encode()
    transport.write(bad_jwt_data)


def handle_add_contact(user_id, username, transport, done_task):
    error = done_task.exception()
    if not error:
        contact_added_data = build_contact_added(username, user_id).json().encode()
        transport.write(contact_added_data)
    else:
        contact_add_error_data = build_add_contact_error(error).json().encode()
        transport.write(contact_add_error_data)


def handle_get_contacts(transport, done_task):
    contacts = done_task.result()
    contacts_result_data = build_get_contacts_result(contacts).json().encode()
    transport.write(contacts_result_data)


def handle_login(username, password, transport, users, connections, done_task):
    user = done_task.result()
    bad_login_data = build_bad_login().json().encode()
    if not user or not user.password == password:
        transport.write(bad_login_data)
    else:
        access, refresh = Token().access_refresh_tokens
        user_id = user.id
        login_done_data = build_send_token(
            "login_done",
            access,
            username,
            user_id
        ).json().encode()
        asyncio.create_task(DB.update_or_create_jwt(user_id, refresh))
        transport.write(login_done_data)
        connections[transport]['username'] = username
        users[username] = connections[transport]
        asyncio.create_task(DB.set_online_status(username, True))


def handle_probe(transport):
    presence = BaseData(command="presence")
    transport.write(presence.json().encode())


def handle_send_msg(user_id, username, transport_from, user_send_to, msg, time):
    send_to = user_send_to["username"] if isinstance(user_send_to, dict) else user_send_to
    msg = Message(
        id=user_id,
        username=username,
        send_to=send_to,
        message=msg,
        send_time=time)

    msg_data = BaseData(command="get_msg", data=msg).json().encode()
    transport_from.write(msg_data)
    if isinstance(user_send_to, dict):
        user_send_to["transport"].write(msg_data)


def handle_get_messages(transport, done_task):
    messages = done_task.result()
    get_messages_result_data = build_get_messages(messages).json().encode()
    transport.write(get_messages_result_data)


def is_authenticated(token, user_id, username, transport):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            access_token = token.access_token
            token_ = Token(token=access_token)
            try:
                token_.verify()
                func(*args, **kwargs)
            except ExpiredSignatureError:
                get_jwt_task = asyncio.create_task(DB.get_jwt(user_id))
                get_jwt_task.add_done_callback(partial(
                    handle_expired_token,
                    user_id,
                    username,
                    transport,
                    func,
                    *args,
                    **kwargs
                ))
            except InvalidSignatureError:
                handle_bad_token(user_id)
        return wrapper
    return decorator
