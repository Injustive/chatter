from sqlalchemy import ForeignKey, Unicode, UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime


CBase = declarative_base()
user_contacts = Table(
    "user_contacts",
    CBase.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("contact_id", Integer, ForeignKey("user.id"), primary_key=True),
)


class User(CBase):
    """Table with clients"""
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    first_name = Column(String(255), default='')
    last_name = Column(String(255), default='')
    signup_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_seen = Column(DateTime, default=None)
    online_status = Column(Boolean(), default=False)
    contacts = relationship(
        "User",
        secondary=user_contacts,
        primaryjoin=id == user_contacts.c.user_id,
        secondaryjoin=id == user_contacts.c.contact_id,
        lazy="joined"
    )

    def add_contact(self, contact):
        if contact not in self.contacts:
            self.contacts.append(contact)
            contact.contacts.append(self)

    def delete_contact(self, contact):
        if contact in self.contacts:
            self.contacts.remove(contact)
            contact.contacts.remove(self)

    def __repr__(self):
        return "{}(username={}, first_name={}, last_name={}, is_online={})".format(
            self.__class__.__name__,
            self.username,
            self.first_name,
            self.last_name,
            self.online_status
        )


class Message(CBase):
    __tablename__ = "message"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id'))
    contact_id = Column(Integer(), ForeignKey('user.id'))
    time = Column(DateTime, nullable=False)
    user = relationship("User", foreign_keys=[user_id], lazy="selectin")
    contact = relationship("User", foreign_keys=[contact_id], lazy="selectin")
    message = Column(Unicode(), nullable=False)

    def __repr__(self):
        return "Message from user {} to user {}. Message text = '{}'".format(
            self.user.username,
            self.contact.username,
            self.message)


class JwtToken(CBase):
    __tablename__ = 'jwt'
    __table_args__ = (
        UniqueConstraint('user_id', name='unique_user'),)

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    token = Column(String(255))