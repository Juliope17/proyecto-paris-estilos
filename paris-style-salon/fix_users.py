import sqlite3
import hashlib

def fix_users():
    """Crear usuarios con credenciales correctas"""
    
    conn = sqlite3.connect('paris_style.db')
    cursor = conn.cursor()
    
    try:
        # Hash para "secreto123"
        password_hash = hashlib.sha256("secreto123".encode()).hexdigest()
        print(f"Hash generado: {password_hash}")
        
        # Eliminar usuarios existentes para evitar duplicados
        cursor.execute("DELETE FROM usuarios")
        
        # Insertar usuarios con credenciales correctas
        users_to_insert = [
            ('Administrador', 'admin@parisstyle.com', '+57 300 000 0000', password_hash, 1),
            ('María García', 'maria.garcia@email.com', '+57 300 123 4567', password_hash, 0),
            ('Carlos Rodríguez', 'carlos.rodriguez@email.com', '+57 300 234 5678', password_hash, 0),
            ('Ana Martínez', 'ana.martinez@email.com', '+57 300 345 6789', password_hash, 0)
        ]
        
        cursor.executemany(
            "INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin) VALUES (?, ?, ?, ?, ?)",
            users_to_insert
        )
        
        conn.commit()
        
        print("✅ Usuarios creados exitosamente:")
        
        # Verificar usuarios creados
        cursor.execute("SELECT nombre, email, es_admin FROM usuarios")
        users = cursor.fetchall()
        
        for user in users:
            role = "Admin" if user[2] else "Usuario"
            print(f"- {user[0]} ({user[1]}) - {role}")
        
        print("\n🔑 Credenciales para probar:")
        print("Email: admin@parisstyle.com")
        print("Password: secreto123")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_users()