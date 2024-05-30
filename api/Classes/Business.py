class Business:
    def __init__(self, name: str, categories: list[str], rating: float, phone: str):
        self.name = name
        self.categories = categories
        self.rating = rating
        self.phone = phone

    def get_name(self) -> str:
        return self.name
    
    def get_categories(self) -> list[str]:
        return self.categories

    def get_rating(self) -> float:
        return self.rating
    
    def get_phone(self) -> str:
        return self.phone
    
    def __str__(self):
        return (
            "name: " + self.name + '\n' +
            str(self.rating) + " stars" + '\n' + 
            "categories: " + str(self.categories) + '\n' +
            "phone: " + self.phone + '\n'
        )
