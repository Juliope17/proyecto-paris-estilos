import sqlite3
import hashlib
import os

def fix_database_complete():
    """Solución completa: recrear DB + insertar datos + configurar usuarios"""
    
    db_path = 'paris_style.db'
    
    print("🔧 SOLUCIONANDO PROBLEMA DE BASE DE DATOS...")
    print("=" * 50)
    
    # Paso 1: Eliminar DB existente
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ 1. Base de datos anterior eliminada")
    
    # Paso 2: Crear nueva estructura
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("✅ 2. Creando nueva estructura...")
        
        # Crear tabla estilistas PRIMERO (para las FK)
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
        
        # Crear tabla usuarios con nuevas columnas
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
                FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
                FOREIGN KEY (estilista_id) REFERENCES estilistas(id),
                FOREIGN KEY (servicio_id) REFERENCES servicios(id)
            )
        """)
        
        print("✅ 3. Insertando estilistas...")
        
        # Insertar estilistas
        estilistas_data = [
            ('María González', 'Corte, Coloración, Tratamientos capilares', '+57 300 111 1111', 'maria@parisstyle.com'),
            ('Ana Rodríguez', 'Manicure, Pedicure, Nail Art', '+57 300 222 2222', 'ana@parisstyle.com'),
            ('Sofía Martínez', 'Maquillaje, Cejas, Pestañas', '+57 300 333 3333', 'sofia@parisstyle.com'),
            ('Lucía Fernández', 'Corte, Peinados, Eventos', '+57 300 444 4444', 'lucia@parisstyle.com')
        ]
        
        cursor.executemany("""
            INSERT INTO estilistas (nombre, especialidades, telefono, email)
            VALUES (?, ?, ?, ?)
        """, estilistas_data)
        
        print("✅ 4. Insertando servicios...")
        
        # Insertar servicios
        servicios_data = [
            ('Corte de Cabello', 'Corte personalizado según tu estilo', 2500000, 45, 'Cabello'),
            ('Coloración Completa', 'Cambio de color completo con productos premium', 4500000, 120, 'Cabello'),
            ('Manicure Clásico', 'Limado, cutícula y esmaltado tradicional', 2000000, 45, 'Uñas'),
            ('Manicure Gel', 'Manicure con esmalte gel de larga duración', 3000000, 60, 'Uñas'),
            ('Maquillaje Social', 'Maquillaje para eventos sociales', 3500000, 45, 'Maquillaje'),
            ('Diseño de Cejas', 'Depilación y diseño profesional de cejas', 1500000, 30, 'Cejas')
        ]
        
        cursor.executemany("""
            INSERT INTO servicios (nombre, descripcion, precio, duracion_minutos, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, servicios_data)
        
        print("✅ 5. Configurando usuarios...")
        
        # Hash para passwords
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        estilista_hash = hashlib.sha256("estilista123".encode()).hexdigest()
        cliente_hash = hashlib.sha256("cliente123".encode()).hexdigest()
        
        # Insertar administrador
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin, es_estilista, estilista_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Administrador', 'admin@parisstyle.com', '+57 300 000 0000', admin_hash, 1, 0, None))
        
        # Insertar usuarios estilistas
        estilistas_usuarios = [
            ('María González', 'maria.gonzalez@parisstyle.com', '+57 300 111 1111', estilista_hash, 0, 1, 1),
            ('Ana Rodríguez', 'ana.rodriguez@parisstyle.com', '+57 300 222 2222', estilista_hash, 0, 1, 2),
            ('Sofía Martínez', 'sofia.martinez@parisstyle.com', '+57 300 333 3333', estilista_hash, 0, 1, 3),
            ('Lucía Fernández', 'lucia.fernandez@parisstyle.com', '+57 300 444 4444', estilista_hash, 0, 1, 4)
        ]
        
        cursor.executemany("""
            INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin, es_estilista, estilista_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, estilistas_usuarios)
        
        # Insertar clientes
        clientes_data = [
            ('María García', 'maria.garcia@email.com', '+57 300 123 4567', cliente_hash, 0, 0, None),
            ('Carlos Rodríguez', 'carlos.rodriguez@email.com', '+57 300 234 5678', cliente_hash, 0, 0, None),
            ('Ana Martínez', 'ana.martinez@email.com', '+57 300 345 6789', cliente_hash, 0, 0, None)
        ]
        
        cursor.executemany("""
            INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin, es_estilista, estilista_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, clientes_data)
        
        conn.commit()
        
        print("✅ 6. Base de datos configurada completamente!")
        print("\n🔑 CREDENCIALES:")
        print("👑 Admin: admin@parisstyle.com / admin123")
        print("💇 Estilista: maria.gonzalez@parisstyle.com / estilista123")
        print("👤 Cliente: maria.garcia@email.com / cliente123")
        print("\n🚀 Ahora ejecuta: python scripts/backend_enhanced.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database_complete()
