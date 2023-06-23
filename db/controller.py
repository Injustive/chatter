from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, values, update, join, or_, and_
from sqlalchemy.orm import joinedload
from db.db_connector import DataAccessLayer
from .models import User, JwtToken, Message
from db.models import CBase
from utils.config import *


class ClientDbHelper:
    def __init__(self, dbpath, base, echo):
        self.dl = DataAccessLayer(dbpath, base, echo)
        self._connected = False

    async def connect_db(self):
        if not self._connected:
            await self.dl.connect()
            self.session = self.dl.create_session()
            self._connected = True
        else:
            raise Exception("Already connected!")

    async def register_user(self, user):
        """Register new user"""
        username = user.username
        if await self.get_user_by_username(username):
            raise ValueError("User {} is already exist".format(username))

        new_user = User(**user.dict())
        self.session.add(new_user)
        await self.session.commit()
        return new_user.id

    async def add_contact(self, user_id, contact_u):
        user = await self.get_user_by_id(user_id)
        contact = await self.get_user_by_username(contact_u)
        if user == contact:
            raise ValueError("You cannot add yourself")
        if not contact:
            raise ValueError("This contact isn't exist")
        if contact in user.contacts:
            raise ValueError("You already have this contact!")
        user.add_contact(contact)
        await self.session.commit()

    async def get_contacts(self, user_id):
        user = await self.get_user_by_id(user_id)
        contacts = user.contacts
        return contacts

    async def write_msg(self, user_id, contact_u, message, time):
        user = await self.get_user_by_id(user_id)
        contact = await self.get_user_by_username(contact_u)
        message = Message(user=user, contact=contact, message=message, time=time)
        self.session.add(message)
        await self.session.commit()

    async def get_all_messages(self, user_id, contact):
        contact = await self.get_user_by_username(contact)
        and_(Message.user_id == user_id, Message.contact == contact)
        and_(Message.user_id == contact.id, Message.contact_id == user_id)
        query = select(Message).where(
            or_(
                and_(
                    Message.user_id == user_id, Message.contact == contact),
                and_(Message.user_id == contact.id, Message.contact_id == user_id)))
        result = await self.session.execute(query)
        messages = result.scalars().all()
        return messages

    async def get_user_by_username(self, username):
        """Get client by its username"""
        query = select(User).options(joinedload(User.contacts)).where(User.username == username)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user

    async def get_user_by_id(self, user_id):
        user = await self.session.get(User, user_id, options=[joinedload(User.contacts)])
        return user

    async def update_or_create_jwt(self, user_id, refresh):
        insert_token = insert(JwtToken).values(user_id=user_id, token=refresh)
        on_duplicate_key = insert_token.on_conflict_do_update(
            index_elements=["user_id"],
            set_=dict(token=refresh),
        )
        await self.session.execute(on_duplicate_key)

    async def get_jwt(self, user_id):
        query = select(JwtToken).where(JwtToken.user_id == user_id)
        result = await self.session.execute(query)
        jwt = result.scalars().first()
        return jwt

    async def delete_jwt(self, user_id):
        query = delete(JwtToken).where(JwtToken.user_id == user_id)
        await self.session.execute(query)
        await self.session.commit()

    async def set_online_status(self, username, status):
        query = update(User).where(User.username == username).values(online_status=status)
        await self.session.execute(query)


DB = ClientDbHelper(DB_DSN, CBase, echo=True)
