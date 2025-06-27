import sqlite3
import os
from datetime import datetime

def setup_database():
    """Configura la base de datos SQLite con todas las tablas y datos iniciales"""
    
    # Eliminar base de datos existente si tiene errores
    db_path = 'paris_style.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Base de datos anterior eliminada")
    
    # Crear nueva conexión
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 Configurando base de datos...")
    
    try:
        # Leer y ejecutar el script de estructura
        print("📋 Creando tablas...")
        with open('scripts/database_setup.sql', 'r', encoding='utf-8') as f:
            setup_script = f.read()
            cursor.executescript(setup_script)
        
        # Leer y ejecutar el script de datos iniciales CORREGIDO
        print("📊 Insertando datos iniciales...")
        seed_file = 'scripts/seed_data_fixed.sql'
        if os.path.exists(seed_file):
            with open(seed_file, 'r', encoding='utf-8') as f:
                seed_script = f.read()
                cursor.executescript(seed_script)
        else:
            print("⚠️ Archivo seed_data_fixed.sql no encontrado, usando el original...")
            with open('scripts/seed_data.sql', 'r', encoding='utf-8') as f:
                seed_script = f.read()
                # Limpiar líneas problemáticas
                seed_script = seed_script.replace("'Maquillaje completo para el día especial', 6000000, 90, 'Maquillaje'),\n('Diseño de Cejas', 'Depil", 
                                                "'Maquillaje completo para el día especial', 6000000, 90, 'Maquillaje'),\n('Diseño de Cejas', 'Depilación y diseño profesional de cejas', 1500000, 30, 'Cejas'),")
                cursor.executescript(seed_script)
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar que las tablas se crearon correctamente
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("✅ Base de datos configurada exitosamente!")
        print(f"📁 Archivo de base de datos: {os.path.abspath(db_path)}")
        print("📋 Tablas creadas:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]}: {count} registros")
        
        # Mostrar credenciales de prueba
        print("\n🔑 Credenciales de prueba:")
        print("👑 Admin: admin@parisstyle.com / secreto123")
        print("👤 Usuario: maria.garcia@email.com / secreto123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error configurando la base de datos: {e}")
        print(f"📍 Error en línea: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()