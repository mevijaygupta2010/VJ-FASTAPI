from email.policy import HTTP
from logging import exception
from pyexpat import model
from xml.dom import ValidationErr
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import oauth2
from .. import models,schemas
from ..database import get_db
from typing import List,Optional

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

my_posts=[{"title": "title of post 1", "content": "content of post 1", "id": 1},{"title": "favorite foods", "content": "I like pizza", "id": 2}]

# @router.get("/sqlalchemy")
# def test_post(db:Session = Depends(get_db)):
#     print("hi")
#     get_posts=db.query(models.Post).all()
#     print(get_posts)
#     return {'data': get_posts}

# @router.get("/",response_model=List[schemas.Post]) #Changed after we brough Votes model
@router.get("/",response_model=List[schemas.PostOut]) #,response_model=List[schemas.PostOut]
def get_posts(db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user), limit: int=10,skip: int =0,search: Optional[str]=""): #Pass the Parameter only for SQL Alchemy
    ###This is when you want to use SQL
    # cursor.execute(""" select * from posts order by id asc; """)
    # posts=cursor.fetchall()
    # print(posts)
    ###This is when you want to use ORM like SQL Alchemy
    try:
        # print(db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        # models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        #     models.Post.title.contains(search)).limit(limit).offset(skip))
        post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    # print(results)
    ###If you want to make all posts public####################
    # posts= db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    # print(limit)
    except ValidationError as e:
        print (e)


    return post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into posts (id,title,content,published) values(%s, %s,%s,%s) RETURNING * """,(post.id,post.title,post.content,post.published))
    # conn.commit()
    # new_post =cursor.fetchone()
    # post_dict=post.dict()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    # print(current_user.email)
    #####SQL ALchemy######
    # print(**post.dict())
    # new_post=models.Post(title=post.title,content=post.content, published=post.published)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
#title as string and content as string and thats all
@router.get("//latest")
def get_latest_posts():
    post_latest=my_posts[len(my_posts)-1]
    return{"detail":post_latest}

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int,response: Response,db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" select * from posts where id=%s """,(str(id),))
    # post=cursor.fetchone()
    # print(post)
    # post =find_post(id)
    ####SQL AlCHEMY#########
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exists")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{'message ': f"post with id: {id} does not exists"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    #deleting posts
    #find the index in the array that has required ID
    #my_posts.pop(index)
    # cursor.execute("""delete from posts where id=%s returning *""",str(id),)
    # deleted_post= cursor.fetchone()
    # index=find_index_post(id)
    # conn.commit()
    ##SQLALCHEMY########
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exists")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authroized to Perform the requested Operation")
    

    # my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_posts(updated_post: schemas.PostCreate,id: int,db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # index=find_index_post(id)
    # cursor.execute(""" update posts set title=%s,content=%s,published=%s where id=%s RETURNING * """,(post.title, post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post =post_query.first()

    # post=post_query.first()
    # print(post_query)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exists")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authroized to Perform the requested Operation")
    
    # post_dict=post.dict()
    
    # post_dict['id']=id
    # my_posts[index]=post_dict
    # print(post)
    post_query.update(updated_post.dict(),synchronize_session= False)
    db.commit()

    return  post_query.first()