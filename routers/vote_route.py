from fastapi import status, HTTPException, APIRouter, Depends
from typing import Annotated
from models import Votes
from schema import Vote
from database import SessionDep
from utils import get_password_hash
from oauth2 import get_current_user
from sqlmodel import select

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, session: SessionDep, current_user = Depends(get_current_user)):

    post = session.get(vote.post_id, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {vote.post_id} does not exist")

    vote_query = select(Votes).where(Votes.post_id == vote.post_id, Votes.user_id == current_user.id)
    found_vote = session.exec(vote_query).first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail= f"User {current_user.id} has already voted on {vote.post_id}")
        
        new_vote = Votes(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return new_vote
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail= "Vote not found")
        
        session.delete(found_vote)
        session.commit()
        return {"message":"Vote deleted successfully"}