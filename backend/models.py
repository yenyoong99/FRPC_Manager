from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(256))
    created_date = Column(DateTime, default=datetime.utcnow)


class FRPManage(Base):
    __tablename__ = "frp_manage"
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(50), unique=True, index=True)
    server_ip = Column(String(15))
    server_port = Column(Integer)
    remote_port = Column(Integer)
    access_token = Column(String(256))
    status = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    process_id = Column(Integer, nullable=True)
