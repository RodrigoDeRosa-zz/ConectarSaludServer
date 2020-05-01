class AuthData:

    def __init__(self, user_id: str, password: str, role: str = None):
        self.user_id = user_id
        self.password = password
        self.role = role
