from pydantic import BaseModel

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attribute = True

class EditorialBase(BaseModel):
    name: str

class EditorialCreate(EditorialBase):
    pass

class Editorial(EditorialBase):
    id: int
    
    class Config:
        from_attribute = True

class AuthorBase(BaseModel):
    name: str

class Author(AuthorBase):
    pass

class BookBase(BaseModel):
    title: str
    pages: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int
    author: Author
    genre_id: int
    genre: Genre
    editorial_id: int
    editorial: Editorial

    class Config:
        from_attributes = True

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    

    class Config:
        from_attributes = True