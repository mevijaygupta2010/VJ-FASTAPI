from fastapi import APIRouter,Depends,status, HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, models,utils,oauth2

router=APIRouter(
    tags=['Authentication']
)
@router.post('/login',response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db:Session = Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email ==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f" Invalid UserName or Password")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f" Invalid UserName or Password")

    #create a token
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    #Return a token
    return {"access_token": access_token, "token_type": "bearer"}
    



