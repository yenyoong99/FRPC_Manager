import os
import subprocess
from sqlalchemy.orm import Session
import models
import schemas
from typing import List


def get_frps_list(db: Session, skip: int = 0, limit: int = 10) -> List[models.FRPManage]:
    return db.query(models.FRPManage).offset(skip).limit(limit).all()


def get_frp(db: Session, frp_id: int):
    return db.query(models.FRPManage).filter(models.FRPManage.id == frp_id).first()


def get_frp_by_client_name(db: Session, client_name: str):
    return db.query(models.FRPManage).filter(models.FRPManage.client_name == client_name).first()


def create_frp(db: Session, frp: schemas.FRPCreate):
    db_frp = models.FRPManage(**frp.dict())
    db.add(db_frp)
    db.commit()
    db.refresh(db_frp)
    return db_frp


def update_frp(db: Session, frp_id: int, frp: schemas.FRPUpdate):
    db_frp = get_frp(db, frp_id)
    for key, value in frp.dict().items():
        setattr(db_frp, key, value)
    db.commit()
    db.refresh(db_frp)
    return db_frp


def delete_frp(db: Session, frp_id: int):
    db_frp = get_frp(db, frp_id)
    db.delete(db_frp)
    db.commit()
    return db_frp


def check_port_in_use(port: int):
    result = subprocess.run(['lsof', '-i', f':{port}'], stdout=subprocess.PIPE)
    return result.returncode == 0


def generate_frps_config(frp: models.FRPManage):
    config = f"""
[common]
bind_port = {frp.server_port}
token = {frp.access_token}
"""
    with open(f"frp_client/{frp.client_name}_frps.ini", "w") as f:
        f.write(config)


def manage_frps_process(frp: models.FRPManage, action: str):
    if action == "start":
        cmd = f"nohup frp_tools/frps -c frp_client/{frp.client_name}_frps.ini  > /dev/null 2>&1 &"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.pid + 1
    elif action == "stop" and frp.process_id:
        os.kill(frp.process_id, 9)
        return None
