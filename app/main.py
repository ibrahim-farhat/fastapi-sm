from fastapi import FastAPI, Response, status, HTTPException

from fastapi.params import Body # to get the body of the post request

from pydantic import BaseModel  # for Pydantic Base Model

from typing import Optional     # for Optional class

from random import randrange    # to generate unique id for each new post

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "frist post", "content": "content of first post", "published": True, "rating": None, "id": 1}, 
            {"title": "second post", "content": "content of second post", "published": True, "rating": None, "id": 2},
            {"title": "third post", "content": "content of third post", "published": True, "rating": None, "id": 3}]

# find the post body with its id
def find_post(id):
    for search_post in my_posts:
        if search_post["id"] == id:
            return search_post
    return None

# find the post index with its id
def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return None

# get all posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def list_posts():
    return my_posts

# create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payLoad: dict = Body(...)):           # old version, without using pydantic library to validate the post schema
def create_post(new_post: Post):
    print(new_post)
    
    new_post_dict = new_post.dict()

    # generate an id for the new post
    new_post_dict["id"] = randrange(0, 1000000)

    # append the new post to my database
    my_posts.append(new_post_dict)

    # debug purpose
    print(new_post_dict)

    # return the new post that was created
    return new_post_dict

# get specific post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    
    # search for the post within our database
    search_index = find_post_index(id)

    # validate that the post is existing
    if search_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found!")
        # return Response(status_code=status.HTTP_404_NOT_FOUND)        # another approach without a detail message
    
    # debug purpose
    print(my_posts[search_index])

    # things are going well, return the post
    return my_posts[search_index]

# update specific post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    # search for the post within our database
    search_index = find_post_index(id)

    # validate that the post is existing
    if search_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # debug purpose
    print(my_posts[search_index])

    # synch our database with the updated post
    updated_post = post.model_dump()
    updated_post["id"] = my_posts[search_index]["id"]
    my_posts[search_index] = updated_post

    # things are going well, return the post after update
    return my_posts[search_index]

# delete specific post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # search for the post within our database
    search_index = find_post_index(id)

    # validate that the post is existing
    if search_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # delete the post
    my_posts.pop(search_index)

    # debug purpose
    print(my_posts[search_index])

    # things are going well, return the response
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# note:
# if you make 2 instances of the same path with the same method,
# your server will go well and the first instance only will be took in consideration.

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/")
# async def root1():
#     return {"message": "Hello Body"}
