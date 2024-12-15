"""Главный модуль"""
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import crud, models, schemas

Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """Главная страница сайта"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    """Получение всех пользователей в формате JSON"""
    return db.query(models.User).all()

@app.get("/users/html", response_class=HTMLResponse)
def read_users_html(request: Request, db: Session = Depends(get_db)):
    """Получение списка пользователей в HTML-формате"""
    users = db.query(models.User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users/create/", response_class=HTMLResponse)
def create_user_form(request: Request):
    """Форма для создания нового пользователя"""
    return templates.TemplateResponse("user_form.html", {"request": request, "user": None})

@app.post("/users/create/")
def create_user_html(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Создание нового пользователя"""
    crud.users.create_user(
    db,
    schemas.UserCreate(username=username, email=email, password=password))
    return {"message": "User created"}

@app.get("/users/edit/{user_id}/", response_class=HTMLResponse)
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    """Форма для редактирования пользователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("user_form.html", {"request": request, "user": user})

@app.post("/users/edit/{user_id}/")
def edit_user_html(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Редактирование данных пользователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    user.username = username
    user.email = email
    user.password = password

    db.commit()
    return {"message": "User updated"}

@app.get("/users/delete/{user_id}/", response_class=HTMLResponse)
def delete_user_html(user_id: int, db: Session = Depends(get_db)):
    """Удаление пользователя"""
    crud.users.delete_user(db, user_id)
    return RedirectResponse(url="/users/html", status_code=303)

@app.get("/posts/")
def get_posts(db: Session = Depends(get_db)):
    """Получение всех постов в формате JSON"""
    return db.query(models.Post).all()

@app.get("/posts/html", response_class=HTMLResponse)
def get_posts_html(request: Request, db: Session = Depends(get_db)):
    """Получение списка постов в HTML-формате"""
    posts = db.query(models.Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

@app.get("/posts/create/", response_class=HTMLResponse)
def create_post_form(request: Request):
    """Форма для создания нового поста"""
    return templates.TemplateResponse("post_form.html", {"request": request, "post": None})

@app.post("/posts/create/")
def create_post_html(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """Создание нового поста"""
    crud.posts.create_post(db, schemas.PostCreate(title=title, content=content, user_id=user_id))
    return RedirectResponse(url="/posts/html", status_code=303)

@app.get("/posts/edit/{post_id}/", response_class=HTMLResponse)
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    """Форма для редактирования поста"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return templates.TemplateResponse("post_form.html", {"request": request, "post": post})

@app.post("/posts/edit/{post_id}/")
def edit_post_html(post_id: int, content: str = Form(...), db: Session = Depends(get_db)):
    """Редактирование содержимого поста"""
    crud.posts.update_post_content(db, post_id, content)
    return RedirectResponse(url="/posts/html", status_code=303)

# Удаление поста (HTML)
@app.get("/posts/delete/{post_id}/", response_class=HTMLResponse)
def delete_post_html(post_id: int, db: Session = Depends(get_db)):
    """Удаление поста"""
    crud.posts.delete_post(db, post_id)
    return RedirectResponse(url="/posts/html", status_code=303)
