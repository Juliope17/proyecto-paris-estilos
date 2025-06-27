import sqlite3
import os
from datetime import datetime

def fix_missing_column_sqlite():
    """Agregar la columna fecha_actualizacion de forma compatible con SQLite"""
    
    db_path = 'paris_style.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔧 Verificando estructura de la tabla citas...")
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(citas)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Columnas actuales en citas: {columns}")
        
        if 'fecha_actualizacion' not in columns:
            print("➕ Agregando columna fecha_actualizacion...")
            
            # Paso 1: Agregar columna sin valor por defecto
            cursor.execute("ALTER TABLE citas ADD COLUMN fecha_actualizacion DATETIME")
            
            # Paso 2: Actualizar registros existentes con la fecha actual
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                UPDATE citas 
                SET fecha_actualizacion = ? 
                WHERE fecha_actualizacion IS NULL
            """, (fecha_actual,))
            
            conn.commit()
            print("✅ Columna fecha_actualizacion agregada exitosamente!")
            print(f"✅ Registros existentes actualizados con fecha: {fecha_actual}")
        else:
            print("✅ La columna fecha_actualizacion ya existe.")
        
        # Verificar estructura final
        cursor.execute("PRAGMA table_info(citas)")
        columns_final = [column[1] for column in cursor.fetchall()]
        print(f"Columnas finales en citas: {columns_final}")
        
        # Mostrar algunos registros para verificar
        cursor.execute("SELECT id, estado, fecha_creacion, fecha_actualizacion FROM citas LIMIT 3")
        registros = cursor.fetchall()
        if registros:
            print("\n📋 Muestra de registros:")
            for registro in registros:
                print(f"  ID: {registro[0]}, Estado: {registro[1]}, Creación: {registro[2]}, Actualización: {registro[3]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_missing_column_sqlite()
