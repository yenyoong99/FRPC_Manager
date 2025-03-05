from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TokenRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class FRPBase(BaseModel):
    client_name: str
    server_ip: str
    server_port: int
    remote_port: int
    access_token: str
    status: bool


class FRPCreate(FRPBase):
    pass


class FRPUpdate(FRPBase):
    pass


class FRP(FRPBase):
    id: int
    created_date: datetime
    updated_date: datetime
    process_id: Optional[int]

    class Config:
        orm_mode = True
