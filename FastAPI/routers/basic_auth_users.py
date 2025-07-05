from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Smith",
        "email": "alice@mail.com",
        "disabled": False,
        "password": "123456"
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Johnson",
        "email": "bob@mail.com",
        "disabled": True,
        "password": "abcdef"
    }
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

@router.get('/users/me', response_model=User)
async def me(user: User = Depends(current_user)):
    return user