from fastapi import status, HTTPException, APIRouter, Depends
from typing import Optional
from app.models import Post, Votes
from sqlmodel import select,col, func
from app.database import SessionDep
from app.schema import PostCreate, PostOut
from app import oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",response_model= list[PostOut])
def get_posts(session:SessionDep, 
              id:int | None = None, 
              current_user = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    
    posts = session.exec(select(Post,func.count(Votes.post_id).label("votes"))
                        .join(Votes, Votes.post_id == Post.id, isouter=True)
                        .where(col(Post.title).ilike(f"%{search}%"))
                        .group_by(Post.id)
                        .limit(limit)
                        .offset(skip)).all()
    return posts



@router.get("/{id}",response_model=PostOut)
def get_posts(session:SessionDep, 
              id:int, 
              current_user = Depends(oauth2.get_current_user)):
    
    post = session.exec(select(Post,func.count(Votes.post_id).label("votes"))
                    .join(Votes, Votes.post_id == Post.id, isouter=True)
                    .where(Post.id == id)
                    .group_by(Post.id)).first()
    if post: 
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")



@router.post("/", status_code=status.HTTP_201_CREATED,response_model=PostCreate)
def create_post(payload : PostCreate, session:SessionDep, current_user = Depends(oauth2.get_current_user)):
    new_post = Post(**payload.model_dump(), user_id=current_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, session:SessionDep, current_user = Depends(oauth2.get_current_user)):
    data = session.get(Post,id)
    if data:
        if data.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail= "Not authorized to perform requested action")
        session.delete(data)
        session.commit()
        return {"Message": f"Deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id : {id} not found")



@router.put("/{id}")
def update_post_put(payload : Post, id :int, session: SessionDep, current_user = Depends(oauth2.get_current_user)):
    data = session.get(Post,id)
    if data:
        if data.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail= "Not authorized to perform requested action")
        update_data = payload.model_dump(exclude_unset=True)
        data.sqlmodel_update(update_data)
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id : {id} not found")