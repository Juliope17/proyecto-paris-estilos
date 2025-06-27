import sqlite3
import hashlib

def setup_enhanced_users():
    """Configurar usuarios con roles específicos"""
    
    conn = sqlite3.connect('paris_style.db')
    cursor = conn.cursor()
    
    try:
        # Agregar columnas si no existen
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN es_estilista BOOLEAN DEFAULT FALSE")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN estilista_id INTEGER")
        except:
            pass  # Las columnas ya existen
        
        # Limpiar usuarios existentes
        cursor.execute("DELETE FROM usuarios")
        
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
        estilistas_data = [
            ('María González', 'maria.gonzalez@parisstyle.com', '+57 300 111 1111', estilista_hash, 0, 1, 1),
            ('Ana Rodríguez', 'ana.rodriguez@parisstyle.com', '+57 300 222 2222', estilista_hash, 0, 1, 2),
            ('Sofía Martínez', 'sofia.martinez@parisstyle.com', '+57 300 333 3333', estilista_hash, 0, 1, 3),
            ('Lucía Fernández', 'lucia.fernandez@parisstyle.com', '+57 300 444 4444', estilista_hash, 0, 1, 4)
        ]
        
        cursor.executemany("""
            INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin, es_estilista, estilista_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, estilistas_data)
        
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
        
        print("✅ Usuarios configurados exitosamente!")
        print("\n🔑 CREDENCIALES:")
        print("\n👑 ADMINISTRADOR:")
        print("Email: admin@parisstyle.com")
        print("Password: admin123")
        
        print("\n💇 ESTILISTAS:")
        print("Email: maria.gonzalez@parisstyle.com | Password: estilista123")
        print("Email: ana.rodriguez@parisstyle.com | Password: estilista123")
        print("Email: sofia.martinez@parisstyle.com | Password: estilista123")
        print("Email: lucia.fernandez@parisstyle.com | Password: estilista123")
        
        print("\n👤 CLIENTES:")
        print("Email: maria.garcia@email.com | Password: cliente123")
        print("Email: carlos.rodriguez@email.com | Password: cliente123")
        print("Email: ana.martinez@email.com | Password: cliente123")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    setup_enhanced_users()
