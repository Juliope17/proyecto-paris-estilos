import sqlite3
import hashlib
import os

def setup_complete_system():
    """Configuración completa del sistema Paris Style"""
    
    db_path = 'paris_style.db'
    
    print("🚀 CONFIGURACIÓN COMPLETA DEL SISTEMA PARIS STYLE")
    print("=" * 60)
    
    # Eliminar DB existente
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Base de datos anterior eliminada")
    
    # Crear nueva DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("✅ Creando estructura de base de datos...")
        
        # Tabla estilistas
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
        
        # Tabla usuarios
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
        
        # Tabla servicios
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
        
        # Tabla citas
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
        
        print("✅ Insertando estilistas...")
        
        # Insertar estilistas
        estilistas = [
            ('María González', 'Corte, Coloración, Tratamientos capilares', '+57 300 111 1111', 'maria@parisstyle.com'),
            ('Ana Rodríguez', 'Manicure, Pedicure, Nail Art', '+57 300 222 2222', 'ana@parisstyle.com'),
            ('Sofía Martínez', 'Maquillaje, Cejas, Pestañas', '+57 300 333 3333', 'sofia@parisstyle.com'),
            ('Lucía Fernández', 'Corte, Peinados, Eventos', '+57 300 444 4444', 'lucia@parisstyle.com')
        ]
        
        cursor.executemany("""
            INSERT INTO estilistas (nombre, especialidades, telefono, email)
            VALUES (?, ?, ?, ?)
        """, estilistas)
        
        print("✅ Insertando servicios...")
        
        # Insertar servicios (precios en centavos)
        servicios = [
            ('Corte de Cabello', 'Corte personalizado según tu estilo', 2500000, 45, 'Cabello'),
            ('Coloración Completa', 'Cambio de color completo con productos premium', 4500000, 120, 'Cabello'),
            ('Mechas', 'Mechas tradicionales o balayage', 3500000, 90, 'Cabello'),
            ('Tratamiento Capilar', 'Hidratación profunda y reparación', 3000000, 60, 'Cabello'),
            ('Peinado para Eventos', 'Peinado elegante para ocasiones especiales', 4000000, 60, 'Cabello'),
            ('Manicure Clásico', 'Limado, cutícula y esmaltado tradicional', 2000000, 45, 'Uñas'),
            ('Manicure Gel', 'Manicure con esmalte gel de larga duración', 3000000, 60, 'Uñas'),
            ('Pedicure Clásico', 'Cuidado completo de pies con esmaltado', 2500000, 60, 'Uñas'),
            ('Pedicure Spa', 'Pedicure relajante con exfoliación y masaje', 3500000, 90, 'Uñas'),
            ('Nail Art', 'Diseños artísticos en uñas', 1500000, 30, 'Uñas'),
            ('Limpieza Facial', 'Limpieza profunda con extracción de impurezas', 3500000, 60, 'Facial'),
            ('Maquillaje Social', 'Maquillaje para eventos sociales', 3500000, 45, 'Maquillaje'),
            ('Maquillaje para Novias', 'Maquillaje completo para el día especial', 6000000, 90, 'Maquillaje'),
            ('Diseño de Cejas', 'Depilación y diseño profesional de cejas', 1500000, 30, 'Cejas'),
            ('Extensiones de Pestañas', 'Aplicación de extensiones pelo a pelo', 4500000, 120, 'Pestañas')
        ]
        
        cursor.executemany("""
            INSERT INTO servicios (nombre, descripcion, precio, duracion_minutos, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, servicios)
        
        print("✅ Configurando usuarios...")
        
        # Passwords
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        estilista_hash = hashlib.sha256("estilista123".encode()).hexdigest()
        cliente_hash = hashlib.sha256("cliente123".encode()).hexdigest()
        
        # Admin
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin, es_estilista, estilista_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Administrador', 'admin@parisstyle.com', '+57 300 000 0000', admin_hash, 1, 0, None))
        
        # Estilistas como usuarios
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
        
        # Clientes
        clientes = [
            ('María García', 'maria.garcia@email.com', '+57 300 123 4567', cliente_hash, 0, 0, None),
            ('Carlos Rodríguez', 'carlos.rodriguez@email.com', '+57 300 234 5678', cliente_hash, 0, 0, None),
            ('Ana Martínez', 'ana.martinez@email.com', '+57 300 345 6789', cliente_hash, 0, 0, None),
            ('Luis Pérez', 'luis.perez@email.com', '+57 300 456 7890', cliente_hash, 0, 0, None),
            ('Carmen López', 'carmen.lopez@email.com', '+57 300 567 8901', cliente_hash, 0, 0, None)
        ]
        
        cursor.executemany("""
            INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin, es_estilista, estilista_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, clientes)
        
        conn.commit()
        
        print("✅ Sistema configurado completamente!")
        print("\n" + "="*60)
        print("🔑 CREDENCIALES DE ACCESO:")
        print("="*60)
        print("\n👑 ADMINISTRADOR:")
        print("   Email: admin@parisstyle.com")
        print("   Password: admin123")
        
        print("\n💇 ESTILISTAS:")
        print("   Email: maria.gonzalez@parisstyle.com | Password: estilista123")
        print("   Email: ana.rodriguez@parisstyle.com | Password: estilista123")
        print("   Email: sofia.martinez@parisstyle.com | Password: estilista123")
        print("   Email: lucia.fernandez@parisstyle.com | Password: estilista123")
        
        print("\n👤 CLIENTES:")
        print("   Email: maria.garcia@email.com | Password: cliente123")
        print("   Email: carlos.rodriguez@email.com | Password: cliente123")
        print("   Email: ana.martinez@email.com | Password: cliente123")
        
        print("\n" + "="*60)
        print("🚀 SIGUIENTE PASO:")
        print("   Ejecuta: python scripts/backend_simple.py")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    setup_complete_system()
