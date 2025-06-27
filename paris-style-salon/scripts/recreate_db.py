import sqlite3
import os

def recreate_database():
    """Eliminar y recrear la base de datos completamente"""
    
    db_path = 'paris_style.db'
    
    # Eliminar base de datos existente
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Base de datos anterior eliminada")
    
    # Crear nueva base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔨 Creando nueva estructura de base de datos...")
        
        # Crear tabla usuarios con todas las columnas
        cursor.execute("""
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                es_admin BOOLEAN DEFAULT FALSE,
                es_estilista BOOLEAN DEFAULT FALSE,
                estilista_id INTEGER,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                activo BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (estilista_id) REFERENCES estilistas(id)
            )
        """)
        
        # Crear tabla estilistas
        cursor.execute("""
            CREATE TABLE estilistas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                especialidades TEXT,
                telefono VARCHAR(20),
                email VARCHAR(100),
                activo BOOLEAN DEFAULT TRUE,
                fecha_contratacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla servicios
        cursor.execute("""
            CREATE TABLE servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                precio INTEGER NOT NULL,
                duracion_minutos INTEGER NOT NULL,
                categoria VARCHAR(50),
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla citas
        cursor.execute("""
            CREATE TABLE citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                estilista_id INTEGER,
                servicio_id INTEGER NOT NULL,
                fecha_hora DATETIME NOT NULL,
                estado VARCHAR(20) DEFAULT 'pendiente',
                notas TEXT,
                precio_total INTEGER,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
                FOREIGN KEY (estilista_id) REFERENCES estilistas(id),
                FOREIGN KEY (servicio_id) REFERENCES servicios(id)
            )
        """)
        
        # Crear índices
        cursor.execute("CREATE INDEX idx_usuarios_email ON usuarios(email)")
        cursor.execute("CREATE INDEX idx_citas_fecha ON citas(fecha_hora)")
        cursor.execute("CREATE INDEX idx_citas_cliente ON citas(cliente_id)")
        cursor.execute("CREATE INDEX idx_citas_estilista ON citas(estilista_id)")
        cursor.execute("CREATE INDEX idx_citas_estado ON citas(estado)")
        
        conn.commit()
        print("✅ Nueva base de datos creada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    recreate_database()
