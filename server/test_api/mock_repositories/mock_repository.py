from abc import ABC, abstractmethod

# NOTE: 
# Same abstract class definition as Repository in the repositories module.
# Redeclared here for cleaner file tree
class MockRepository[T](ABC):
    @abstractmethod
    def get(self, email: str) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, email: str, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, email: str) -> None:
        raise NotImplementedError
    
    