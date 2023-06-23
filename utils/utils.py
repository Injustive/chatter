import binascii
import hashlib
import jwt
from datetime import datetime, timedelta
from utils.config import JWT_SECRET, JWT_REFRESH_TTL, JWT_ACCESS_TTL


def hash_password(password):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                             'salt'.encode('utf-8'), 100000)
    hashed_password = binascii.hexlify(dk)
    return hashed_password


class Token:
    def __init__(self,
                 token=None,
                 secret=JWT_SECRET,
                 access_ttl=JWT_REFRESH_TTL,
                 refresh_ttl=JWT_ACCESS_TTL):
        self.token = token
        self.secret = secret
        self.access_ttl = access_ttl
        self.refresh_ttl = refresh_ttl

    @property
    def access_refresh_tokens(self):
        access = self.get_access_token()
        refresh = self.get_refresh_token()
        return access, refresh

    def get_access_token(self):
        access_payload = {
            'exp': datetime.utcnow() + timedelta(seconds=self.access_ttl),
            'type': 'access'
        }
        access = jwt.encode(payload=access_payload, key=self.secret)
        return access

    def get_refresh_token(self):
        refresh_payload = {
            'exp': datetime.utcnow() + timedelta(seconds=self.refresh_ttl),
            'type': 'refresh'
        }
        refresh = jwt.encode(payload=refresh_payload, key=self.secret)
        return refresh

    def verify(self):
        jwt.decode(self.token, self.secret, algorithms=["HS256"])



