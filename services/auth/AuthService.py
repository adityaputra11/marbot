from services.auth.AuthRepository import AuthRepository

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def register(self, username: str, name: str):
        return self.auth_repository.register(username, name)

    def login(self, username: str):
        return self.auth_repository.login(username)
    
    def subscribe(self, username: str):
        return self.auth_repository.subscribe(username)