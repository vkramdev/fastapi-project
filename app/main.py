from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel

from random import randrange

app=FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool =True
    rating: Optional[int] = None

#This is temporary way to create ,delete and update untill the posts are stored in
#DB
all_post = [{"title":"This is post one", "content":"dummy content", "id":1},
            {"title":"This is post two", "content":"dummy content two", "id":2}]

def get_single_post(id):
    post_to_send=""
    for p in all_post:
        if p['id']== id:
            post_to_send=p

    return post_to_send

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    return {'data':all_post}

#First post method check
@app.post("/posttest")
def create_post(payload:dict = Body(...)):  ## what does this Body(...) refer to
    print(payload)
    return{'new_message': f'This is post about title: {payload["title"]}, content: {payload["content"]}'}

#Initial post creation 
@app.post("/createposts")
def create_post(new_post : Post):
    print(new_post)
    print(new_post.rating)
    print(new_post.model_dump())
    return {'message' : new_post}

'''
#path operations should be plurals.
@app.post("/posts")
def create_posts(post: Post):
    post_dict= post.model_dump()
    post_dict['id'] = randrange(1,9999999)
    all_post.append(post_dict)
    return {"data" : post_dict}
'''

#Changing the default status code to 201 for creation
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict= post.model_dump()
    post_dict['id'] = randrange(1,9999999)
    all_post.append(post_dict)
    return {"data" : post_dict}

#Retrieving a single post with the help of id. Id is called "path parameter"
@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    post_to_send=get_single_post(int(id))
    if not post_to_send:
        #response.status_code=404
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {"data" : post_to_send}

'''
#Path order is important in FastAPI. 
#The @app.get("/posts/{id}") will match path in this commented code
# FastAPI reads paths from top to down. 
@app.get("/posts/latest")
def get_post():
    latest_post=all_post[len(all_post)-1]
    return {"data" : latest_post}
'''

#Delete post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    del_idx= False
    for i, p in enumerate(all_post):
        if p['id']==id:
            del all_post[i]
            del_idx= True
            break
    if del_idx:
        Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} not found")
    
#update post
@app.put("/posts/{id}")
def update_post(id: int,post: Post):
    update_post=False
    post_dict=post.model_dump()
    for i,p in enumerate(all_post):
        if p['id']==id:
            post_dict['id']=id
            all_post[i]=post_dict
            update_post=True
        else:
            pass

    if update_post:
        return {'data':post_dict}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id : {id} not found")