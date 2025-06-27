import sqlite3
import hashlib

def check_users():
    """Verificar usuarios en la base de datos"""
    
    conn = sqlite3.connect('paris_style.db')
    cursor = conn.cursor()
    
    try:
        # Obtener todos los usuarios
        cursor.execute("SELECT id, nombre, email, password_hash, es_admin FROM usuarios")
        users = cursor.fetchall()
        
        print("=== USUARIOS EN LA BASE DE DATOS ===")
        for user in users:
            print(f"ID: {user[0]}")
            print(f"Nombre: {user[1]}")
            print(f"Email: {user[2]}")
            print(f"Hash: {user[3]}")
            print(f"Admin: {user[4]}")
            print("-" * 40)
        
        # Verificar hash de "secreto123"
        test_password = "secreto123"
        expected_hash = hashlib.sha256(test_password.encode()).hexdigest()
        print(f"Hash esperado para 'secreto123': {expected_hash}")
        
        # Verificar si algún usuario tiene este hash
        cursor.execute("SELECT email FROM usuarios WHERE password_hash = ?", (expected_hash,))
        matching_users = cursor.fetchall()
        
        if matching_users:
            print(f"Usuarios con password 'secreto123': {[u[0] for u in matching_users]}")
        else:
            print("❌ Ningún usuario tiene el password 'secreto123'")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_users()