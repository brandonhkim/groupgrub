from uuid import uuid4
from dataclasses import dataclass
from .mock_repository import MockRepository

@dataclass
class User:
    id: str
    email: str
    password: str
    preferences: dict

    def __init__(self, email: str, password: str, preferences: dict, id: str=None):
        self.id = id if id else uuid4().hex
        self.email = email
        self.password = password
        self.preferences = preferences


class MockUserRepository(MockRepository[User]):
    def __init__(self, users: dict = None) -> None:
        self.users_id = users or {}
        self.users_email = {}
        if users:
            for user in users:
                self.users_email[user.email] = user

    def get(self, id: str="", email:str="") -> User:
        if id and id in self.users_id:
            return self.users_id[id]
        if email and email in self.users_email: 
            return self.users_email[email]
        return None
    
    def get_all(self) -> list[User]:
        return NotImplementedError
    
    def add(self, **kwargs: object) -> None:
        id = kwargs['id']
        email = kwargs['email']
        password = kwargs['password']
        preferences = kwargs['preferences']

        user = User(id=id, email=email, password=password, preferences=preferences)

        self.users_id[id] = user
        self.users_email[email] = user
    
    def update(self, id: str, email: str, **kwargs: object) -> None:
        if id not in self.users_id or email not in self.users_email:
            return
        
        old_user = self.users_id[id] if id else self.users_email[email]
        password = old_user.password
        old_user.preferences.update(kwargs['new_preferences'])
        preferences = old_user.preferences

        user = User(id=id, email=email, password=password, preferences=preferences)
        
        self.users_id[id] = user
        self.users_email[email] = user
    
    def update_password(self, id: str, email: str, **kwargs: object) -> None:
        if id not in self.users_id or email not in self.users_email:
            return
        
        old_user = self.users_id[id] if id else self.users_email[email]
        preferences = old_user.preferences
        new_password = kwargs['new_password']

        user = User(id=id, email=email, password=new_password, preferences=preferences)
        
        self.users_id[id] = user
        self.users_email[email] = user
    
    def delete(self, id: str, email: str="") -> None:
        del self.users_id[id]
        del self.users_email[email]
        
        