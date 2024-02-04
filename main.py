from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models, schemas, hashing
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError


SECRET_KEY = "56a37c720ff058a1f052458f0426c5fae86fb0bbde710dfdedda52a14e8c762a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
    return {"token": token}

########################AUTHOR#############################################

@app.post("/authors/", response_model=schemas.Author)
async def createAuthor(author: schemas.AuthorCreate, db: Session = Depends(getDb)):
    author_db = crud.getAuthorByName(db=db, author_name=author.name)
    if author_db:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.createAuthor(db=db, author=author)

@app.get("/authors/", response_model=list[schemas.Author])
async def readAuthors(skip:int = 0, limit: int = 100, db: Session = Depends(getDb)):
    return crud.getAuthors(db=db)

@app.get("/authors/{author_id}", response_model=schemas.Author)
async def readAuthor(author_id: int, db: Session = Depends(getDb)):
    db_author = crud.getAuthor(db=db, author_id = author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

########################BOOK#############################################

@app.get("/books/", response_model=list[schemas.Book])
async def readBooks(skip:int = 0, limit: int = 100, db: Session = Depends(getDb)):
    return crud.getBooks(db=db)

@app.get("/listbooks/{author_id}", response_model=list[schemas.Book])
async def readBooksByAuthor(author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(getDb)):
    return crud.getBooksByAuthor(author_id=author_id, db=db)

@app.post("/books/", response_model=schemas.Book)
async def createBook(genre_id: int, author_id:int, editorial_id: int, book: schemas.BookCreate, db: Session = Depends(getDb)):
    return crud.createBook(db=db, book=book, author_id=author_id, genre_id=genre_id, editorial_id=editorial_id)

@app.get("/books/{book_id}", response_model=schemas.Book)
async def readBook(book_id: int, db: Session = Depends(getDb)):
    return crud.getBook(book_id=book_id, db=db)


##################GENRE###################################

@app.post("/genres/", response_model=schemas.Genre)
async def createGenre(genre: schemas.GenreCreate, db: Session = Depends(getDb)):
    genre_db = crud.getGenreByName(db=db, genre_name=genre.name)
    if genre_db:
        raise HTTPException(status_code=400, detail="Genre already exists")
    return crud.createGenre(db=db, genre=genre)

@app.get("/books/genre/{genre_id}", response_model=list[schemas.Book])
async def readBooksByGenre(genre_id: int, db: Session = Depends(getDb)):
    return crud.getBooksByGenreName(db=db, genre_id=genre_id)


####################EDITORIAL####################################

@app.post("/editorials/", response_model=schemas.Editorial)
async def createEditorial(editorial: schemas.EditorialCreate, db: Session = Depends(getDb)):
    editorial_db = crud.getEditorialByName(db=db, editorial_name=editorial.name)
    if editorial_db:
        raise HTTPException(status_code=400, detail="Editorial already exists")
    return crud.createEditorial(db=db, editorial=editorial)

@app.get("/editorials/", response_model=list[schemas.Editorial])
async def readEditorials(db: Session = Depends(getDb)):
    return crud.getEditorials(db=db)

@app.get("/books/editorial/{editorial_id}", response_model=list[schemas.Book])
async def readBooksByEditorial(editorial_id: int, db: Session = Depends(getDb)):
    return crud.getBooksByEditorial(db=db, editorial_id=editorial_id)

@app.get("/editorials/{editorial_id}", response_model=schemas.Editorial)
async def readEditorial(editorial_id: int, db: Session = Depends(getDb)):
    return crud.getEditorial(db=db, editorial_id=editorial_id)

############## USER #############

@app.post("/register/", response_model=schemas.User)
async def createUser(user: schemas.UserCreate, db: Session = Depends(getDb)):
    user.password = hashing.get_password_hash(user.password)
    return crud.createUser(db=db, user=user)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDb)):
    user = crud.getUserByName(db=db, user_name=form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not hashing.authenticate_user(user=user, username=form_data.username, password=form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(getDb)):
    user = crud.getUserByName(db=db, user_name=token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@app.get("/users/me/")
async def getCurrentMe(db:Session = Depends(getDb), user: schemas.User = Depends(getCurrentUser)):
    return {"hashed_pass": hashing.get_password_hash(user.password)}