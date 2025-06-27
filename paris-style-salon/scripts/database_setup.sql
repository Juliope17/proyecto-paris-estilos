-- Crear base de datos para Paris Style
-- Este script configura la estructura inicial de la base de datos

-- Tabla de usuarios/clientes
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de estilistas
CREATE TABLE IF NOT EXISTS estilistas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    especialidades TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_contratacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de servicios
CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio INTEGER NOT NULL, -- Precio en centavos para evitar problemas de decimales
    duracion_minutos INTEGER NOT NULL,
    categoria VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de citas
CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    estilista_id INTEGER,
    servicio_id INTEGER NOT NULL,
    fecha_hora DATETIME NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente', -- pendiente, confirmada, completada, cancelada
    notas TEXT,
    precio_total INTEGER, -- Precio final de la cita
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
    FOREIGN KEY (estilista_id) REFERENCES estilistas(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

-- Tabla de horarios de trabajo de estilistas
CREATE TABLE IF NOT EXISTS horarios_trabajo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estilista_id INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL, -- 0=Domingo, 1=Lunes, etc.
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (estilista_id) REFERENCES estilistas(id)
);

-- Tabla de notificaciones
CREATE TABLE IF NOT EXISTS notificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    cita_id INTEGER,
    tipo VARCHAR(50) NOT NULL, -- recordatorio, confirmacion, cancelacion
    mensaje TEXT NOT NULL,
    enviado BOOLEAN DEFAULT FALSE,
    fecha_envio DATETIME,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (cita_id) REFERENCES citas(id)
);

-- Tabla de productos (para la tienda)
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio INTEGER NOT NULL,
    stock INTEGER DEFAULT 0,
    categoria VARCHAR(50),
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_citas_fecha ON citas(fecha_hora);
CREATE INDEX IF NOT EXISTS idx_citas_cliente ON citas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_citas_estilista ON citas(estilista_id);
CREATE INDEX IF NOT EXISTS idx_citas_estado ON citas(estado);
CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario ON notificaciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_notificaciones_enviado ON notificaciones(enviado);
