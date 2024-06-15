from dataclasses import dataclass
from .mock_repository import MockRepository

@dataclass
class Preference:
    id: str
    email: str
    preferences: set

    def __init__(self, id: str, email: str, preferences: set):
        self.id = id
        self.email = email
        self.preferences = preferences


class MockPreferenceRepository(MockRepository[Preference]):
    def __init__(self, preferences: dict = None) -> None:
        self.preferences = preferences or {}

    def get(self, id: str="", email: str="") -> Preference:
        if id not in self.preferences:
            return None
        
        return self.preferences[id]
    
    def get_all(self) -> list[Preference]:
        return NotImplementedError
    
    def add(self, **kwargs: object) -> None:
        id = kwargs['id']
        preference = Preference(id=id, email=kwargs['email'], preferences=kwargs['preferences'])

        self.preferences[id] = preference
    
    def update(self, id: str, email: str, **kwargs: object) -> dict:
        old_preferences = self.preferences[id].preferences

        new_preferences = old_preferences.union(set(kwargs["new_preferences"]))

        self.preferences[id].preferences = new_preferences

        return {
            "preferences": new_preferences
        }
    
    def delete(self, id: str, email: str="") -> None:
        del self.preferences[id]
        
        