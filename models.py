from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), index=True)
    pages = Column(Integer, index=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    genre_id = Column(Integer, ForeignKey("genre.id"))
    editorial_id = Column(Integer, ForeignKey("editorial.id"))

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    editorial = relationship("Editorial", back_populates="books")
    association_book = relationship("AssociationUserBook", back_populates="book")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)

    books = relationship("Book", back_populates="author")

class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)

    books = relationship("Book", back_populates="genre")


class Editorial(Base):
    __tablename__ = "editorial"

    id = Column(Integer, primary_key = True)
    name = Column(String(50), index=True)

    books = relationship("Book", back_populates="editorial")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), index=True)
    email = Column(String(50), index=True)
    password = Column(String(100), index=True)

    association_user = relationship("AssociationUserBook", back_populates="user")

class AssociationUserBook(Base):
    __tablename__ = "association_user_book"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    readed = Column(Boolean, index=True)

    user = relationship("User", back_populates="association_user")
    book = relationship("Book", back_populates="association_book")


