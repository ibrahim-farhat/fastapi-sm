from fastapi import FastAPI, Response, status, HTTPException

from fastapi.params import Body # to get the body of the post request

from pydantic import BaseModel  # for Pydantic Base Model

from typing import Optional     # for Optional class

from random import randrange    # to generate unique id for each new post

import psycopg2                                 # to deal with postgres database

from psycopg2.extras import RealDictCursor      # to deal with postgres database

import time                     # to make delays


# initiate the fastapi application
app = FastAPI()


# connect to the postgres database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='28122000', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database was successfully connected.")
        break
    
    except Exception as error:
        print("Database can't be connected!")
        print("Error: ", error)
        time.sleep(2)

# create a class for posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None      # was for demonstration purposes


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
    # get all the posts from the database
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    # return all the posts to the client
    return {"data": posts}

# create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    print(new_post)
    
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (new_post.title, new_post.content, new_post.published))
    new_post_dict = cursor.fetchone()
    conn.commit()

    # debug purpose
    print(new_post_dict)

    # return the new post that was created
    return {"data": new_post_dict}

# get specific post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    
    # search for the post within our database
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id), ))
    database_response = cursor.fetchone()

    # validate that the post is existing
    if not database_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found!")
    
    # debug purpose
    print(database_response)

    # things are going well, return the post
    return {"data": database_response}

# update specific post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):

    # search for the post within our database, and update it if it is found
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
                   (post.title, post.content, post.published, str(id)))
    database_response = cursor.fetchone()
    
    # validate that the post is existing
    if not database_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # synch our database with the updated post
    conn.commit()

    # debug purpose
    print(database_response)
    
    # things are going well, return the post after update
    return {"data": database_response}

# delete specific post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # search for the post within our database, and delete it if it is found
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id), ))
    database_response = cursor.fetchone()

    # validate that the post is existing
    if not database_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # synch our database with the updated post
    conn.commit()

    # debug purpose
    print(database_response)

    # things are going well, return the response
    return Response(status_code=status.HTTP_204_NO_CONTENT)