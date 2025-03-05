from fastapi import FastAPI, Depends, HTTPException, status, Body, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
import models
import schemas
import database
import crud
import auth
import uvicorn
from typing import List

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), tr: schemas.TokenRequest = Body(...), ):
    user = auth.authenticate_user(db, tr.username, tr.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/frp/", response_model=schemas.FRP)
def create_frp(frp: schemas.FRPCreate, db: Session = Depends(get_db),
               current_user: schemas.User = Depends(auth.get_current_user)):
    if crud.check_port_in_use(frp.server_port) or crud.check_port_in_use(frp.remote_port):
        raise HTTPException(status_code=400, detail="Port already in use")
    db_frp = crud.create_frp(db=db, frp=frp)
    crud.generate_frps_config(db_frp)
    if db_frp.status:
        db_frp.process_id = crud.manage_frps_process(db_frp, "start")
        db.commit()
        db.refresh(db_frp)
    return db_frp


@app.get("/frp/{frp_id}", response_model=schemas.FRP)
def read_frp(frp_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_frp = crud.get_frp(db, frp_id=frp_id)
    if db_frp is None:
        raise HTTPException(status_code=404, detail="FRP not found")
    return db_frp


@app.put("/frp/{frp_id}", response_model=schemas.FRP)
def update_frp(frp_id: int, frp: schemas.FRPUpdate, db: Session = Depends(get_db),
               current_user: schemas.User = Depends(auth.get_current_user)):
    db_frp = crud.get_frp(db, frp_id=frp_id)
    if db_frp is None:
        raise HTTPException(status_code=404, detail="FRP not found")
    if frp.status and not db_frp.status:
        db_frp.process_id = crud.manage_frps_process(db_frp, "start")
    elif not frp.status and db_frp.status:
        crud.manage_frps_process(db_frp, "stop")
        db_frp.process_id = None
    db_frp = crud.update_frp(db, frp_id=frp_id, frp=frp)
    return db_frp


@app.delete("/frp/{frp_id}", response_model=schemas.FRP)
def delete_frp(frp_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_frp = crud.get_frp(db, frp_id=frp_id)
    if db_frp.status:
        crud.manage_frps_process(db_frp, "stop")
    return crud.delete_frp(db, frp_id=frp_id)


@app.get("/frps/", response_model=List[schemas.FRP])
def list_frps(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db),
              current_user: schemas.User = Depends(auth.get_current_user)):
    frps = crud.get_frps_list(db, skip=skip, limit=limit)
    return frps


if __name__ == '__main__':
    uvicorn.run('main:app')
