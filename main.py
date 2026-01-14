from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api.route.user_routers import router as user_router
from app.exceptions import UserNotFoundError, EmailNotAllowedNameExistsError
from app.core.logging_config import log_http
from app.core.db import pool

app = FastAPI()
app.middleware("http")(log_http)

from app.exceptions import add_exception_handlers

add_exception_handlers(app)


from app.api.route.chat_routers import router as chat_router
from app.api.route.todo_routers import router as todo_router
app.include_router(user_router)
app.include_router(todo_router)
app.include_router(chat_router)