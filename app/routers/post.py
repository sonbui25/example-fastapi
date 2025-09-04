from sqlalchemy import func
from .. import models, schemas, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).\
        filter(models.Post.title.contains(search)).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
        limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # post_id = find_post(id)
    # if not post_id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id: {id} was not found")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": "Post not found"}
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,)) # Lưu ý dấu phẩy sau id
    # post_id = cursor.fetchone()
    # post_id = db.query(models.Post).filter(models.Post.id == id).first()
    post_id = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).\
        filter(models.Post.id == id).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).first()
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return post_id

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit() # Nhớ là phải commit
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    # update_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post_query.first()