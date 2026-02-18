from fastapi import status, HTTPException, APIRouter, Depends
from typing import Annotated
from app.models import User
from app.schema import UserCreate, UserOut
from app.database import SessionDep
from app.utils import get_password_hash
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def read_user( current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(payload : UserCreate, session:SessionDep):
    payload.password = get_password_hash(payload.password)
    new_user = User.model_validate(payload)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=UserOut)
def get_user (id : int, sessions: SessionDep):
    data = sessions.get(User,id)
    if data: 
        return data 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id : {id} not found")