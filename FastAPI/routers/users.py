from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"], prefix="/users", responses={404: {"message": "Not found"}})

# entidad: User
# atributos: name, surname, url
# descripción: User entity with attributes name, surname, and url


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str


users_list = [
    User(
        id=1,
        name="Alice",
        surname="Smith",
        age=30,
        url="https://example.com/users/alice",
    ),
    User(
        id=2, name="Bob", surname="Johnson", age=25, url="https://example.com/users/bob"
    ),
    User(
        id=3,
        name="Charlie",
        surname="Brown",
        age=35,
        url="https://example.com/users/charlie",
    ),
]


@router.get("/usersjson")
async def usersjson():
    return {
        "users": [
            {
                "name": "Alice",
                "surname": "Smith",
                "age": 30,
                "url": "https://example.com/users/alice",
            },
            {
                "name": "Bob",
                "surname": "Johnson",
                "age": 25,
                "url": "https://example.com/users/bob",
            },
            {
                "name": "Charlie",
                "surname": "Brown",
                "age": 35,
                "url": "https://example.com/users/charlie",
            },
        ]
    }


@router.get("/")
async def users():
    return users_list


@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


@router.get("/userquery")
async def userq(id: int):
    return search_user(id)

@router.post("/", response_model= User,status_code=201)
async def create_user(user: User):
    if isinstance(search_user(user.id), User):
        raise HTTPException(status_code=204, detail="User already exists")
    users_list.routerend(user)
    return user

@router.put("/")
async def update_user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "User not found"}
    else:
        return user

@router.delete("/{id}")
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            found = True
            del users_list[index]
            return {"message": "User deleted"}
    if not found:
        return {"error": "User not found"}

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": "User not found"}