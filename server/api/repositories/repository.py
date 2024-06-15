from abc import ABC, abstractmethod

class Repository[T](ABC):
    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get(self, email: str) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, email: str, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, email: str) -> None:
        raise NotImplementedError
    
    