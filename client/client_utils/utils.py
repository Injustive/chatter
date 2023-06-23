class CurrentToken:
    def __init__(self, token=None):
        self.token = token


class CurrentUser:
    def __init__(self, id_=None, username=None):
        self.id_ = id_
        self.username = username


current_token = CurrentToken()
current_user = CurrentUser()
