from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Text
from pydantic import BaseModel, ConfigDict
from typing import List
from database import Base, get_db, create_tables
import uvicorn

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Post 모델
class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

# Pydantic 스키마
class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str

# 테이블 생성
create_tables()

@app.get('/')
def home():
    return {'message': 'Post API Server'}

# Create
@app.post('/posts', response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Read All
@app.get('/posts', response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

# Read One
@app.get('/posts/{post_id}', response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Update
@app.put('/posts/{post_id}', response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

# Delete
@app.delete('/posts/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {'message': 'Post deleted successfully'}

if __name__ == '__main__':
    uvicorn.run('main:app',
                host='127.0.0.1',
                port=8000,
                reload=True)