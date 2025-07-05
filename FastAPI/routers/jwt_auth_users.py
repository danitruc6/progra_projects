from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
SECRET = "3981c39afb8295c9a68f2730953ea5515b8c2358aa5feabc45d176623dee67af"
ACCESS_TOKEN_DURATION = 1

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


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
        "password": "$2a$12$rE996YooW/D2iV8ZHdyh5eIFJJ2co3XyvpS5RDnW9akDCy/4ppCIC",
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Johnson",
        "email": "bob@mail.com",
        "disabled": True,
        "password": "$2a$12$FxLDMPbbQPtxjqRsnqg4DeKx0LDcmX1GvVn6ixghhVJNA/8TdT3Uy",
    },
}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except jwt.PyJWTError:
        raise exception
    return search_user(username) 


async def current_user(user: User = Depends(auth_user)):
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }
    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


@router.get("/users/me", response_model=User)
async def me(user: User = Depends(current_user)):
    return user
