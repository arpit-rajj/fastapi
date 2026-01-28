from fastapi import Depends, status,HTTPException, APIRouter
from sqlalchemy.orm import Session 
from ..databases import get_db
from .. import models , schema , oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def do_vote(vote:schema.Vote, db: Session = Depends (get_db),
             current_user : int = Depends(oauth2.get_current_user)):
    post_found = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if(not post_found):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {vote.post_id} does not exist")
    if(vote.dir==1):
        exist_vote = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,
                                                  models.Vote.user_id==current_user.id).first()
        if(exist_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="user has already voted on this post")
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message":"successfully added vote"}
    if(vote.dir==0):
        exist_vote = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,
                                                 models.Vote.user_id==current_user.id).first()
        if(not exist_vote):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote does not exist")
        db.delete(exist_vote)
        db.commit()
        return {"message":"successfully deleted vote"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="invalid vote direction. should be 0 or 1")
    
