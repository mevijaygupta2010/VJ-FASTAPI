from fastapi.testclient import TestClient
from app.main import app
from app import schemas

import pytest
from jose import JWTError, jwt
from app.config import settings





# def test_root(client):

#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Welcome to my coolest Api!!'

def test_create_user(client):
    res=client.post("/users/",json={"email":"maci@gmail.com","password":"password123"})   
    schemas.UserOut(**res.json())
    assert res.json().get("email") == "maci@gmail.com"
    assert res.status_code==201

def test_login_user(client,test_user):
    res=client.post("/login", data=  {"username":test_user['email'],"password":test_user['password']})
    login_res =schemas.Token(**res.json())
    payload= jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id= payload.get("user_id")
    assert id ==test_user['id']
    assert login_res.token_type =='bearer'
    assert res.status_code ==200
@pytest.mark.parametrize("email,password,status_code",[
    ('wrongemail@gmail.com','password123',403),
    ('vijay@gmail.com','wrongpassword',403),
    (None,'password123',422),
    ('vijay@gmail.com',None,422)
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res=client.post("/login",data ={"username":email,"password":password})
    assert res.status_code ==status_code
    #assert res.json().get('detail') ==' Invalid UserName or Password'


