from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import crud, models, schemas

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI()

# Подключение шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===== Главная страница =====

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ===== API и HTML-интерфейсы для пользователей =====

# Получение всех пользователей (JSON)
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Управление пользователями (HTML)
@app.get("/users/html", response_class=HTMLResponse)
def read_users_html(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Создание пользователя (HTML форма)
@app.get("/users/create/", response_class=HTMLResponse)
def create_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request, "user": None})

@app.post("/users/create/")
def create_user_html(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    crud.users.create_user(db, schemas.UserCreate(username=username, email=email, password=password))
    return {"message": "User created"}


# Редактирование пользователя (HTML форма)
@app.get("/users/edit/{user_id}/", response_class=HTMLResponse)
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_form.html", {"request": request, "user": user})

# Редактирование пользователя
@app.post("/users/edit/{user_id}/")
def edit_user_html(user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Находим пользователя по ID
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем данные пользователя
    user.username = username
    user.email = email
    user.password = password

    # Сохраняем изменения в базе данных
    db.commit()

    return {"message": "User updated"}



# Удаление пользователя (HTML)
@app.get("/users/delete/{user_id}/", response_class=HTMLResponse)
def delete_user_html(user_id: int, db: Session = Depends(get_db)):
    if not crud.users.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse(url="/users/html", status_code=303)

# ===== API и HTML-интерфейсы для постов =====

# Получение всех постов (JSON)
@app.get("/posts/")
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

# Управление постами (HTML)
@app.get("/posts/html", response_class=HTMLResponse)
def get_posts_html(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

# Создание поста (HTML форма)
@app.get("/posts/create/", response_class=HTMLResponse)
def create_post_form(request: Request):
    return templates.TemplateResponse("post_form.html", {"request": request, "post": None})

@app.post("/posts/create/")
def create_post_html(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    try:
        crud.posts.create_post(db, schemas.PostCreate(title=title, content=content, user_id=user_id))
        return RedirectResponse(url="/posts/html", status_code=303)
    except Exception as e:
        return {"error": str(e)}

# Редактирование поста (HTML форма)
@app.get("/posts/edit/{post_id}/", response_class=HTMLResponse)
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post_form.html", {"request": request, "post": post})

@app.post("/posts/edit/{post_id}/")
def edit_post_html(post_id: int, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    crud.posts.update_post_content(db, post_id, content)
    return RedirectResponse(url="/posts/html", status_code=303)

# Удаление поста (HTML)
@app.get("/posts/delete/{post_id}/", response_class=HTMLResponse)
def delete_post_html(post_id: int, db: Session = Depends(get_db)):
    if not crud.posts.delete_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return RedirectResponse(url="/posts/html", status_code=303)
