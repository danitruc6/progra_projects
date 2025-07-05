from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    tags=["userdb"],
    prefix="/userdb",
    responses={status.HTTP_401_UNAUTHORIZED: {"message": "Not found"}},
)

# entidad: User
# atributos: name, surname, url
# descripción: User entity with attributes name, surname, and url

users_list = []


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/")
async def userq(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if isinstance(search_user("email", user.email), User):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already exists")

    user_dict = dict(user)
    del user_dict["id"]  # Remove id to let the database generate it
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))
    return User(**new_user)


@router.put("/", response_model=User)
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]  # Remove id to let the database use the existing one
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    
    except:
        return {"error": "User not updated, user not found"}
    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "User not found"}


def search_user(field: str, key):
    user = db_client.users.find_one({field: key})
    if user is None:
        return {"error": "User not found"}
    try:
        return User(**user_schema(user))
    except IndexError:
        return {"error": "User not found"}

