from fastapi import FastAPI, Depends, APIRouter
from config import engine, db_dependency
from schemas import RequestTask
import models
import auth
import crud


app = FastAPI(title="Junior Test App")

router = APIRouter()


@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)


@router.post('/create')
async def create(request: RequestTask, db: db_dependency, current_user: auth.user_dependency):
    return crud.create_task(db, request.parameter, current_user)


@router.get("/")
async def get(db: db_dependency, current_user: auth.user_dependency):
    _task = crud.get_task(db, current_user)
    return _task


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(router, prefix="/task", tags=["task"], dependencies=[Depends(auth.get_current_user)])
