
from typing import List, Optional
from fastapi import Depends, status,Response,HTTPException, APIRouter
from sqlalchemy import func
from .. import models , schema , oauth2
from ..databases import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schema.Postwithvote]) 
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM post""")
    # my_posts = cursor.fetchall()
    # my_posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id, 
    #                                         models.Post.content.contains(search)).limit(limit).offset(skip).all()
    my_posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(
            models.Post.owner_id==current_user.id, 
            models.Post.content.contains(search)).limit(limit).offset(skip).all()   
    return my_posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schema.Postresponse)
def create_post(post: schema.createpost , db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO post (title, content,rating, published) 
    #                VALUES (%s, %s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.rating, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/all", response_model=List[schema.Postwithvote])
def get_all_posts(db:Session = Depends (get_db),limit:int=10):
    all_posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).limit(limit).all()
    return all_posts

@router.get("/{id}", response_model=schema.Postresponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM post WHERE id = %s""",(str(id),))
    # get_one_post = cursor.fetchone()
    # if not get_one_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f"post with id {id} not found")
    get_one_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not get_one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    return get_one_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()   
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id {id} not found")
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Postresponse)
def update_post(id: int, updated_post: schema.createpost, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE post SET title = %s, content = %s, rating = %s,
    #                published = %s WHERE id = %s RETURNING *""",
    #                (updated_post.title, updated_post.content, updated_post.rating,
    #                 updated_post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post_id = db.query(models.Post).filter(models.Post.id == id) #query to 
                                                                        #find the index
    found_post = updated_post_id.first() #variable to check if post exists 
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    if found_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    updated_post_id.update(updated_post.dict())
    db.commit()
    return updated_post_id.first()