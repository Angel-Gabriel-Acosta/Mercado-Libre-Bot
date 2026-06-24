from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///mlbot.db")
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    access_token = Column(String)
    refresh_token = Column(String)
    nickname = Column(String)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def guardar_usuario(user_id, access_token, refresh_token, nickname=""):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.user_id == str(user_id)).first()
    if usuario:
        usuario.access_token = access_token
        usuario.refresh_token = refresh_token
        usuario.nickname = nickname
    else:
        usuario = Usuario(
            user_id=str(user_id),
            access_token=access_token,
            refresh_token=refresh_token,
            nickname=nickname
        )
        db.add(usuario)
    db.commit()
    db.close()

def obtener_usuario(user_id):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.user_id == str(user_id)).first()
    db.close()
    return usuario

def obtener_primer_usuario():
    db = SessionLocal()
    usuario = db.query(Usuario).first()
    db.close()
    return usuario