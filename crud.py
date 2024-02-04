from sqlalchemy.orm import Session

import models, schemas

def createAuthor(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def getAuthors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def getAuthor(db: Session, author_id):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def getAuthorByName(db: Session, author_name):
    return db.query(models.Author).filter(models.Author.name == author_name).first()

####################### BOOK ############################################

def createBook(db: Session, book: schemas.BookCreate, author_id: int, genre_id: int, editorial_id: int):
    db_book = models.Book(**book.model_dump(), author_id=author_id, genre_id=genre_id, editorial_id=editorial_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def getBooks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def getBooksByAuthor(author_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(models.Book.author_id == author_id).offset(skip).limit(limit).all()

def getBook(db:Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


####################### GENRE ###############################################

def createGenre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def getGenres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

def getBooksByGenreName(genre_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(models.Book.genre_id == genre_id).offset(skip).limit(limit).all()

def getGenreByName(db: Session, genre_name: str):
    return db.query(models.Genre).filter(models.Genre.name == genre_name).first()


############## EDITORIAL ####################################

def createEditorial(db: Session, editorial: schemas.EditorialCreate):
    db_editorial = models.Editorial(name=editorial.name)
    db.add(db_editorial)
    db.commit()
    db.refresh(db_editorial)
    return db_editorial

def getBooksByEditorial(db: Session, editorial_id: int, skip = 0, limit = 100):
    return db.query(models.Book).filter(models.Book.editorial_id == editorial_id).offset(skip).limit(limit).all()

def getEditorials(db: Session, skip = 0, limit = 100):
    return db.query(models.Editorial).offset(skip).limit(limit).all()

def getEditorial(db: Session, editorial_id: int):
    return db.query(models.Editorial).filter(models.Editorial.id == editorial_id).first()

def getEditorialByName(db: Session, editorial_name: str):
    return db.query(models.Editorial).filter(models.Editorial.name == editorial_name).first()

############## USER ################

def createUser(db:Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def getUser(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def getUserByName(db: Session, user_name: int):
    return db.query(models.User).filter(models.User.name == user_name).first()