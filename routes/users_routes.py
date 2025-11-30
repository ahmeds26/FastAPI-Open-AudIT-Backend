from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import timedelta 
from typing import Annotated
from helpers.authenticate import *
from server.config import ACCESS_TOKEN_EXPIRE_MINUTES
from models.user import *
from server.database import db_connect
import mysql.connector


users_router = APIRouter()

@users_router.post("/signup", response_description="User Sign Up", status_code=status.HTTP_201_CREATED, response_model=User)
async def sign_up(user: CreateUser, db: mysql.connector.connection.MySQLConnection = Depends(db_connect)) -> JSONResponse:

    # Check if user exists
    cursor = db.cursor()
    query = "SELECT id FROM users WHERE email = %s"
    cursor.execute(query, (user.email,))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user
    query = "INSERT INTO users (email, hashed_password) VALUES (%s, %s)"
    values = (user.email, hashed_password)
    cursor.execute(query, values)
    db.commit()
    
    # Return user
    new_user = User(
        id=cursor.lastrowid,
        email=user.email,
        hashed_password=hashed_password
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_user))

@users_router.post("/request-token", response_description="Generate Access Token", status_code=status.HTTP_200_OK)
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(Token(access_token=access_token, token_type="bearer")))
