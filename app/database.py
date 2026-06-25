from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

engine = create_engine("sqlite:///mlbot.db")
Base = declarative_base()
ph = PasswordHasher()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    ml_user_id = Column(String)
    ml_access_token = Column(String)
    ml_refresh_token = Column(String)
    ml_nickname = Column(String)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def registrar_usuario(email: str, password: str):
    db = SessionLocal()
    existente = db.query(Usuario).filter(Usuario.email == email).first()
    if existente:
        db.close()
        return None
    hash = ph.hash(password)
    usuario = Usuario(email=email, password_hash=hash)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    db.close()
    return usuario

def login_usuario(email: str, password: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    db.close()
    if not usuario:
        return None
    try:
        ph.verify(usuario.password_hash, password)
        return usuario
    except VerifyMismatchError:
        return None

def guardar_ml_token(user_id: int, ml_user_id: str, access_token: str, refresh_token: str, nickname: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if usuario:
        usuario.ml_user_id = str(ml_user_id)
        usuario.ml_access_token = access_token
        usuario.ml_refresh_token = refresh_token
        usuario.ml_nickname = nickname
        db.commit()
    db.close()

def obtener_usuario_por_id(user_id: int):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    db.close()
    return usuario

def obtener_usuario_por_ml_id(ml_user_id: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.ml_user_id == str(ml_user_id)).first()
    db.close()
    return usuario

class Configuracion(Base):
    __tablename__ = "configuraciones"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, unique=True)
    tono = Column(String, default="amigable")
    info_extra = Column(String, default="")
    bot_activo = Column(Integer, default=1)
    modo_revision = Column(Integer, default=0)

Base.metadata.create_all(engine)

def obtener_config(usuario_id: int):
    db = SessionLocal()
    config = db.query(Configuracion).filter(Configuracion.usuario_id == usuario_id).first()
    if not config:
        config = Configuracion(usuario_id=usuario_id, tono="amigable", info_extra="", bot_activo=1, modo_revision=0)
        db.add(config)
        db.commit()
        db.refresh(config)
    db.close()
    return config

def guardar_config(usuario_id: int, tono: str, info_extra: str, bot_activo: bool, modo_revision: bool):
    db = SessionLocal()
    config = db.query(Configuracion).filter(Configuracion.usuario_id == usuario_id).first()
    if not config:
        config = Configuracion(usuario_id=usuario_id)
        db.add(config)
    config.tono = tono
    config.info_extra = info_extra
    config.bot_activo = 1 if bot_activo else 0
    config.modo_revision = 1 if modo_revision else 0
    db.commit()
    db.close()

class Historial(Base):
    __tablename__ = "historial"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)
    pregunta = Column(String)
    respuesta = Column(String)
    producto = Column(String)
    fecha = Column(String, default=lambda: datetime.now().strftime("%d/%m/%Y %H:%M"))

Base.metadata.create_all(engine)

def guardar_historial(usuario_id: int, pregunta: str, respuesta: str, producto: str):
    db = SessionLocal()
    item = Historial(usuario_id=usuario_id, pregunta=pregunta, respuesta=respuesta, producto=producto)
    db.add(item)
    db.commit()
    db.close()

def obtener_historial(usuario_id: int):
    db = SessionLocal()
    items = db.query(Historial).filter(Historial.usuario_id == usuario_id).order_by(Historial.id.desc()).all()
    db.close()
    return items