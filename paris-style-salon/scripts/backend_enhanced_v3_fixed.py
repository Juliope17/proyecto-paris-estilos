from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import hashlib
import jwt
import uvicorn

# Configuración
DATABASE_URL = "sqlite:///./paris_style.db"
SECRET_KEY = "SECRET_KEY_PARIS_STYLE_2024"
ALGORITHM = "HS256"

# Base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
security = HTTPBearer()

# Modelos de base de datos
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    es_admin = Column(Boolean, default=False)
    es_estilista = Column(Boolean, default=False)
    estilista_id = Column(Integer, ForeignKey("estilistas.id"), nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now)
    
    citas = relationship("Cita", back_populates="cliente")

class Estilista(Base):
    __tablename__ = "estilistas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especialidades = Column(Text)
    activo = Column(Boolean, default=True)
    
    citas = relationship("Cita", back_populates="estilista")

class Servicio(Base):
    __tablename__ = "servicios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    precio = Column(Integer, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    categoria = Column(String)
    activo = Column(Boolean, default=True)
    
    citas = relationship("Cita", back_populates="servicio")

class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estilista_id = Column(Integer, ForeignKey("estilistas.id"), nullable=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String, default="pendiente")
    notas = Column(Text)
    precio_total = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now)
    
    cliente = relationship("Usuario", back_populates="citas")
    estilista = relationship("Estilista", back_populates="citas")
    servicio = relationship("Servicio", back_populates="citas")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Modelos Pydantic
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    telefono: str
    password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str

class CitaCreate(BaseModel):
    servicio_id: int
    estilista_id: Optional[int] = None
    fecha_hora: str
    notas: Optional[str] = None

class CitaUpdate(BaseModel):
    estado: str

# FastAPI app
app = FastAPI(
    title="Paris Style API Enhanced v3 Fixed", 
    version="3.0.1",
    description="Sistema de gestión de citas para salón de belleza - Sin dependencias externas"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def parse_datetime_safe(datetime_str: str) -> datetime:
    """Convierte string de fecha a datetime de forma segura usando solo stdlib"""
    try:
        print(f"Parsing datetime string: {datetime_str}")
        
        # Limpiar el string de timezone info
        clean_str = datetime_str.replace('Z', '').replace('+00:00', '')
        
        # Intentar diferentes formatos
        formats = [
            "%Y-%m-%dT%H:%M:%S",      # 2025-06-21T14:00:00
            "%Y-%m-%dT%H:%M",         # 2025-06-21T14:00
            "%Y-%m-%d %H:%M:%S",      # 2025-06-21 14:00:00
            "%Y-%m-%d %H:%M",         # 2025-06-21 14:00
            "%Y-%m-%dT%H:%M:%S.%f",   # 2025-06-21T14:00:00.000
        ]
        
        for fmt in formats:
            try:
                result = datetime.strptime(clean_str, fmt)
                print(f"Successfully parsed with format {fmt}: {result}")
                return result
            except ValueError:
                continue
        
        # Si ningún formato funciona, intentar fromisoformat
        try:
            result = datetime.fromisoformat(clean_str)
            print(f"Successfully parsed with fromisoformat: {result}")
            return result
        except ValueError:
            pass
        
        raise ValueError(f"No se pudo parsear el formato de fecha: {datetime_str}")
        
    except Exception as e:
        print(f"Error parsing datetime: {datetime_str}, error: {e}")
        raise ValueError(f"Formato de fecha inválido: {datetime_str}")

def asignar_estilista_automatico(servicio_id: int, fecha_hora: datetime, db: Session) -> Optional[int]:
    """Asigna automáticamente un estilista disponible para el servicio"""
    try:
        estilistas = db.query(Estilista).filter(Estilista.activo == True).all()
        
        for estilista in estilistas:
            conflicto = db.query(Cita).filter(
                and_(
                    Cita.estilista_id == estilista.id,
                    Cita.fecha_hora == fecha_hora,
                    Cita.estado.in_(["pendiente", "confirmada"])
                )
            ).first()
            
            if not conflicto:
                return estilista.id
        
        return None
    except Exception as e:
        print(f"Error asignando estilista: {e}")
        return None

# Endpoints
@app.get("/")
def read_root():
    return {
        "message": "Paris Style API Enhanced v3 Fixed funcionando!", 
        "status": "OK",
        "version": "3.0.1",
        "fixes": ["Datetime comparison fixed", "No external dependencies", "Better error handling"]
    }

@app.post("/api/auth/register")
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        
        hashed_password = hash_password(user.password)
        db_user = Usuario(
            nombre=user.nombre,
            email=user.email,
            telefono=user.telefono,
            password_hash=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {"message": "Usuario registrado exitosamente", "user_id": db_user.id}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error en registro: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/api/auth/login")
def login_user(user: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
        
        if not db_user or not verify_password(user.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        access_token = create_access_token({
            "user_id": db_user.id,
            "email": db_user.email,
            "es_admin": db_user.es_admin,
            "es_estilista": db_user.es_estilista
        })
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "nombre": db_user.nombre,
                "email": db_user.email,
                "es_admin": db_user.es_admin,
                "es_estilista": db_user.es_estilista,
                "estilista_id": db_user.estilista_id
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/api/servicios")
def get_servicios(db: Session = Depends(get_db)):
    try:
        servicios = db.query(Servicio).filter(Servicio.activo == True).all()
        return servicios
    except Exception as e:
        print(f"Error obteniendo servicios: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo servicios")

@app.get("/api/estilistas")
def get_estilistas(db: Session = Depends(get_db)):
    try:
        estilistas = db.query(Estilista).filter(Estilista.activo == True).all()
        return estilistas
    except Exception as e:
        print(f"Error obteniendo estilistas: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo estilistas")

@app.post("/api/citas")
def create_cita(cita: CitaCreate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        print(f"Creando cita para usuario: {current_user.nombre}")
        print(f"Datos recibidos: {cita}")
        
        # Verificar servicio
        servicio = db.query(Servicio).filter(Servicio.id == cita.servicio_id).first()
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        
        # Convertir fecha de forma segura
        try:
            fecha_hora = parse_datetime_safe(cita.fecha_hora)
            print(f"Fecha convertida exitosamente: {fecha_hora}")
        except ValueError as e:
            print(f"Error en conversión de fecha: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        
        # Verificar que no sea en el pasado
        ahora = datetime.now()
        print(f"Comparando: {fecha_hora} > {ahora}")
        if fecha_hora <= ahora:
            raise HTTPException(status_code=400, detail="No puedes agendar citas en el pasado")
        
        estilista_id = cita.estilista_id
        
        # Si se especificó estilista, verificar disponibilidad
        if estilista_id and estilista_id > 0:
            estilista = db.query(Estilista).filter(Estilista.id == estilista_id).first()
            if not estilista:
                raise HTTPException(status_code=404, detail="Estilista no encontrado")
            
            # Verificar conflictos
            conflicto = db.query(Cita).filter(
                and_(
                    Cita.estilista_id == estilista_id,
                    Cita.fecha_hora == fecha_hora,
                    Cita.estado.in_(["pendiente", "confirmada"])
                )
            ).first()
            
            if conflicto:
                raise HTTPException(
                    status_code=400, 
                    detail=f"El estilista {estilista.nombre} ya tiene una cita en ese horario"
                )
        else:
            # Asignar estilista automáticamente
            estilista_id = asignar_estilista_automatico(cita.servicio_id, fecha_hora, db)
            if not estilista_id:
                raise HTTPException(
                    status_code=400, 
                    detail="No hay estilistas disponibles en ese horario"
                )
        
        # Crear cita
        db_cita = Cita(
            cliente_id=current_user.id,
            estilista_id=estilista_id,
            servicio_id=cita.servicio_id,
            fecha_hora=fecha_hora,
            notas=cita.notas,
            precio_total=servicio.precio,
            estado="pendiente"
        )
        
        db.add(db_cita)
        db.commit()
        db.refresh(db_cita)
        
        # Obtener nombre del estilista asignado
        estilista_asignado = db.query(Estilista).filter(Estilista.id == estilista_id).first()
        
        print(f"Cita creada exitosamente: ID {db_cita.id}")
        
        return {
            "message": "Cita creada exitosamente",
            "cita_id": db_cita.id,
            "fecha_hora": db_cita.fecha_hora.isoformat(),
            "servicio": servicio.nombre,
            "estilista": estilista_asignado.nombre if estilista_asignado else "No asignado",
            "precio": servicio.precio,
            "estado": "pendiente"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error creando cita: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/api/citas")
def get_citas(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        query = db.query(Cita).join(Usuario, Cita.cliente_id == Usuario.id).join(Servicio, Cita.servicio_id == Servicio.id)
        
        if current_user.es_admin:
            citas = query.all()
        elif current_user.es_estilista:
            citas = query.filter(Cita.estilista_id == current_user.estilista_id).all()
        else:
            citas = query.filter(Cita.cliente_id == current_user.id).all()
        
        result = []
        for cita in citas:
            estilista_nombre = None
            if cita.estilista:
                estilista_nombre = cita.estilista.nombre
            
            # Determinar permisos
            puede_confirmar = False
            puede_cancelar = False
            puede_completar = False
            
            if current_user.es_estilista and cita.estilista_id == current_user.estilista_id:
                puede_confirmar = cita.estado == "pendiente"
                puede_completar = cita.estado == "confirmada"
            elif current_user.es_admin:
                puede_confirmar = cita.estado == "pendiente"
                puede_cancelar = cita.estado in ["pendiente", "confirmada"]
                puede_completar = cita.estado == "confirmada"
            elif cita.cliente_id == current_user.id:
                puede_cancelar = cita.estado in ["pendiente", "confirmada"]
            
            result.append({
                "id": cita.id,
                "cliente_nombre": cita.cliente.nombre,
                "cliente_email": cita.cliente.email,
                "cliente_telefono": cita.cliente.telefono,
                "estilista_nombre": estilista_nombre,
                "servicio_nombre": cita.servicio.nombre,
                "fecha_hora": cita.fecha_hora.isoformat(),
                "estado": cita.estado,
                "notas": cita.notas,
                "precio_total": cita.precio_total,
                "fecha_creacion": cita.fecha_creacion.isoformat(),
                "puede_confirmar": puede_confirmar,
                "puede_cancelar": puede_cancelar,
                "puede_completar": puede_completar
            })
        
        return result
    
    except Exception as e:
        print(f"Error obteniendo citas: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo citas")

@app.put("/api/citas/{cita_id}")
def update_cita(cita_id: int, cita_update: CitaUpdate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        cita = db.query(Cita).filter(Cita.id == cita_id).first()
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        
        nuevo_estado = cita_update.estado
        
        # Validar permisos y transiciones
        if nuevo_estado == "confirmada":
            if not (current_user.es_admin or (current_user.es_estilista and cita.estilista_id == current_user.estilista_id)):
                raise HTTPException(status_code=403, detail="Solo el estilista asignado puede confirmar esta cita")
            if cita.estado != "pendiente":
                raise HTTPException(status_code=400, detail="Solo se pueden confirmar citas pendientes")
        
        elif nuevo_estado == "cancelada":
            if not (current_user.es_admin or 
                   cita.cliente_id == current_user.id or 
                   (current_user.es_estilista and cita.estilista_id == current_user.estilista_id)):
                raise HTTPException(status_code=403, detail="No tienes permisos para cancelar esta cita")
            if cita.estado not in ["pendiente", "confirmada"]:
                raise HTTPException(status_code=400, detail="No se puede cancelar una cita ya completada o cancelada")
        
        elif nuevo_estado == "completada":
            if not (current_user.es_admin or (current_user.es_estilista and cita.estilista_id == current_user.estilista_id)):
                raise HTTPException(status_code=403, detail="Solo el estilista asignado puede completar esta cita")
            if cita.estado != "confirmada":
                raise HTTPException(status_code=400, detail="Solo se pueden completar citas confirmadas")
        
        else:
            raise HTTPException(status_code=400, detail="Estado no válido")
        
        # Actualizar estado
        cita.estado = nuevo_estado
        cita.fecha_actualizacion = datetime.now()
        db.commit()
        
        return {
            "message": f"Cita {nuevo_estado} exitosamente",
            "cita_id": cita.id,
            "nuevo_estado": nuevo_estado
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error actualizando cita: {e}")
        raise HTTPException(status_code=500, detail="Error actualizando cita")

@app.get("/api/user/profile")
def get_user_profile(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "telefono": current_user.telefono,
        "es_admin": current_user.es_admin,
        "es_estilista": current_user.es_estilista,
        "estilista_id": current_user.estilista_id
    }

@app.get("/api/estilistas/{estilista_id}/disponibilidad")
def get_disponibilidad_estilista(estilista_id: int, fecha: str, db: Session = Depends(get_db)):
    """Obtener horarios ocupados de un estilista en una fecha específica"""
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        
        citas_ocupadas = db.query(Cita).filter(
            and_(
                Cita.estilista_id == estilista_id,
                Cita.fecha_hora >= datetime.combine(fecha_obj, datetime.min.time()),
                Cita.fecha_hora < datetime.combine(fecha_obj, datetime.min.time()) + timedelta(days=1),
                Cita.estado.in_(["pendiente", "confirmada"])
            )
        ).all()
        
        horarios_ocupados = [cita.fecha_hora.strftime("%H:%M") for cita in citas_ocupadas]
        
        return {
            "estilista_id": estilista_id,
            "fecha": fecha,
            "horarios_ocupados": horarios_ocupados
        }
    
    except Exception as e:
        print(f"Error obteniendo disponibilidad: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo disponibilidad")

if __name__ == "__main__":
    print("🚀 Iniciando Paris Style API Enhanced v3 Fixed...")
    print("📋 Documentación: http://127.0.0.1:8000/docs")
    print("🌐 API: http://127.0.0.1:8000")
    print("\n🔧 FUNCIONALIDADES:")
    print("✅ Datetime comparison FIXED (sin dependencias externas)")
    print("✅ Solo estilistas pueden confirmar citas")
    print("✅ Citas asignadas por estilista")
    print("✅ Clientes pueden cancelar citas")
    print("✅ Validación de horarios ocupados")
    print("✅ Mejor logging para debugging")
    uvicorn.run("__main__:app", host="127.0.0.1", port=8000, reload=True)
