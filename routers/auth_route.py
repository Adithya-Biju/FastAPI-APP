from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from utils import verify_password
from database import SessionDep
from models import User
from sqlmodel import select
from oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schema import Token

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(session:SessionDep, payload : Annotated[OAuth2PasswordRequestForm, Depends()]):

    statement = select(User).where(User.email == payload.username)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_password(payload.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    data = {"user_id":user.id}
    access_token = create_access_token(data)
    return {"access_token":access_token,"token_type":"bearer"}