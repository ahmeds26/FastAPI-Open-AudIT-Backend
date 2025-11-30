from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    id: int
    email: str | None = None
    hashed_password: str

class CreateUser(BaseModel):
    email: str
    password: str

class UserInDB(User):
    hashed_password: str

