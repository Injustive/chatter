from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field
from utils.utils import hash_password


class User(BaseModel):
    id: Union[int, None]
    username: str
    password: str
    first_name: str
    last_name: str

    def __init__(self, **data):
        super().__init__(**data)
        self.password = hash_password(data["password"])


class Login(BaseModel):
    username: str
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        self.password = hash_password(data["password"])


class UserUsername(BaseModel):
    id: int
    username: str


class UserContact(UserUsername):
    contact: str


class Message(UserUsername):
    send_to: str
    message: str
    send_time: datetime = Field(default_factory=datetime.utcnow)


class Jwt(BaseModel):
    access_token: str


class Error(BaseModel):
    error: str


class Contact(BaseModel):
    username: str
    first_name: str
    last_name: str
    online_status: bool
    signup_date: datetime
    last_seen: Union[datetime, None]

    class Config:
        orm_mode = True


class Msg(BaseModel):
    time: datetime
    user: Contact
    contact: Contact
    message: str

    class Config:
        orm_mode = True


class MessagesList(BaseModel):
    messages: list[Msg]


class ContactsList(BaseModel):
    contacts: list[Contact]


class BaseData(BaseModel):
    command: str
    data:  Union[Message,
                 UserContact,
                 UserUsername,
                 User,
                 Login,
                 Error,
                 ContactsList,
                 MessagesList,
                 None]
    token: Union[Jwt, None]


class BaseParser:
    def __init__(self, bdata):
        self.raw_data = bdata.decode()
        self.parsed_data = None
        self.parse()

    def parse(self):
        self.parsed_data = BaseData.parse_raw(self.raw_data)

    @property
    def command(self):
        return self.parsed_data.command

    @property
    def data(self):
        return self.parsed_data.data

    @property
    def token(self):
        return self.parsed_data.token

    @property
    def jwt(self):
        return getattr(self.parsed_data, "jwt")
