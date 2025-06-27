-- Datos iniciales para Paris Style
-- Este script inserta datos de ejemplo para probar el sistema

-- Insertar estilistas
INSERT INTO estilistas (nombre, especialidades, telefono, email) VALUES
('María González', 'Corte, Coloración, Tratamientos capilares', '+57 300 111 1111', 'maria@parisstyle.com'),
('Ana Rodríguez', 'Manicure, Pedicure, Nail Art', '+57 300 222 2222', 'ana@parisstyle.com'),
('Sofía Martínez', 'Maquillaje, Cejas, Pestañas', '+57 300 333 3333', 'sofia@parisstyle.com'),
('Lucía Fernández', 'Corte, Peinados, Eventos', '+57 300 444 4444', 'lucia@parisstyle.com');

-- Insertar servicios de cabello
INSERT INTO servicios (nombre, descripcion, precio, duracion_minutos, categoria) VALUES
('Corte de Cabello', 'Corte personalizado según tu estilo', 2500000, 45, 'Cabello'),
('Coloración Completa', 'Cambio de color completo con productos premium', 4500000, 120, 'Cabello'),
('Mechas', 'Mechas tradicionales o balayage', 3500000, 90, 'Cabello'),
('Tratamiento Capilar', 'Hidratación profunda y reparación', 3000000, 60, 'Cabello'),
('Peinado para Eventos', 'Peinado elegante para ocasiones especiales', 4000000, 60, 'Cabello'),
('Lavado y Secado', 'Lavado con productos profesionales y secado', 1500000, 30, 'Cabello');

-- Insertar servicios de uñas
INSERT INTO servicios (nombre, descripcion, precio, duracion_minutos, categoria) VALUES
('Manicure Clásico', 'Limado, cutícula y esmaltado tradicional', 2000000, 45, 'Uñas'),
('Manicure Gel', 'Manicure con esmalte gel de larga duración', 3000000, 60, 'Uñas'),
('Pedicure Clásico', 'Cuidado completo de pies con esmaltado', 2500000, 60, 'Uñas'),
('Pedicure Spa', 'Pedicure relajante con exfoliación y masaje', 3500000, 90, 'Uñas'),
('Nail Art', 'Diseños artísticos en uñas', 1500000, 30, 'Uñas'),
('Uñas Acrílicas', 'Extensión de uñas con acrílico', 4000000, 90, 'Uñas');

-- Insertar servicios faciales y maquillaje
INSERT INTO servicios (nombre, descripcion, precio, duracion_minutos, categoria) VALUES
('Limpieza Facial', 'Limpieza profunda con extracción de impurezas', 3500000, 60, 'Facial'),
('Maquillaje Social', 'Maquillaje para eventos sociales', 3500000, 45, 'Maquillaje'),
('Maquillaje para Novias', 'Maquillaje completo para el día especial', 6000000, 90, 'Maquillaje'),
('Diseño de Cejas', 'Depil  'Maquillaje completo para el día especial', 6000000, 90, 'Maquillaje'),
('Diseño de Cejas', 'Depilación y diseño profesional de cejas', 1500000, 30, 'Cejas'),
('Extensiones de Pestañas', 'Aplicación de extensiones pelo a pelo', 4500000, 120, 'Pestañas'),
('Tinte de Cejas', 'Coloración de cejas para mayor definición', 1200000, 20, 'Cejas'),
('Microblading', 'Técnica de micropigmentación para cejas', 15000000, 180, 'Cejas');

-- Insertar horarios de trabajo (Lunes a Sábado, 9:00 AM - 6:00 PM)
INSERT INTO horarios_trabajo (estilista_id, dia_semana, hora_inicio, hora_fin) VALUES
-- María González (ID: 1)
(1, 1, '09:00', '18:00'), -- Lunes
(1, 2, '09:00', '18:00'), -- Martes
(1, 3, '09:00', '18:00'), -- Miércoles
(1, 4, '09:00', '18:00'), -- Jueves
(1, 5, '09:00', '18:00'), -- Viernes
(1, 6, '09:00', '17:00'), -- Sábado

-- Ana Rodríguez (ID: 2)
(2, 1, '09:00', '18:00'),
(2, 2, '09:00', '18:00'),
(2, 3, '09:00', '18:00'),
(2, 4, '09:00', '18:00'),
(2, 5, '09:00', '18:00'),
(2, 6, '09:00', '17:00'),

-- Sofía Martínez (ID: 3)
(3, 1, '09:00', '18:00'),
(3, 2, '09:00', '18:00'),
(3, 3, '09:00', '18:00'),
(3, 4, '09:00', '18:00'),
(3, 5, '09:00', '18:00'),
(3, 6, '09:00', '17:00'),

-- Lucía Fernández (ID: 4)
(4, 1, '09:00', '18:00'),
(4, 2, '09:00', '18:00'),
(4, 3, '09:00', '18:00'),
(4, 4, '09:00', '18:00'),
(4, 5, '09:00', '18:00'),
(4, 6, '09:00', '17:00');

-- Insertar productos para la tienda
INSERT INTO productos (nombre, descripcion, precio, stock, categoria, imagen_url) VALUES
('Shampoo Profesional', 'Shampoo hidratante para todo tipo de cabello', 2500000, 50, 'Cuidado Capilar', '/images/shampoo.jpg'),
('Acondicionador Reparador', 'Acondicionador para cabello dañado', 2800000, 45, 'Cuidado Capilar', '/images/acondicionador.jpg'),
('Mascarilla Nutritiva', 'Tratamiento intensivo semanal', 3500000, 30, 'Cuidado Capilar', '/images/mascarilla.jpg'),
('Esmalte Gel Premium', 'Esmalte de larga duración en varios colores', 1800000, 100, 'Uñas', '/images/esmalte.jpg'),
('Kit de Manicure', 'Set completo para manicure en casa', 4500000, 25, 'Uñas', '/images/kit-manicure.jpg'),
('Base de Maquillaje', 'Base líquida de cobertura media', 3200000, 40, 'Maquillaje', '/images/base.jpg'),
('Paleta de Sombras', 'Paleta con 12 tonos neutros', 2800000, 35, 'Maquillaje', '/images/sombras.jpg'),
('Sérum Facial', 'Sérum hidratante con ácido hialurónico', 4200000, 20, 'Cuidado Facial', '/images/serum.jpg');

-- Insertar usuario administrador
INSERT INTO usuarios (nombre, email, telefono, password_hash, es_admin) VALUES
('Administrador', 'admin@parisstyle.com', '+57 300 000 0000', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', TRUE);

-- Insertar algunos usuarios de ejemplo
INSERT INTO usuarios (nombre, email, telefono, password_hash) VALUES
('María García', 'maria.garcia@email.com', '+57 300 123 4567', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'),
('Carlos Rodríguez', 'carlos.rodriguez@email.com', '+57 300 234 5678', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'),
('Ana Martínez', 'ana.martinez@email.com', '+57 300 345 6789', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f');

-- Insertar algunas citas de ejemplo
INSERT INTO citas (cliente_id, estilista_id, servicio_id, fecha_hora, estado, notas, precio_total) VALUES
(2, 1, 1, '2024-01-20 10:00:00', 'confirmada', 'Cliente prefiere corte moderno', 2500000),
(3, 2, 8, '2024-01-22 14:30:00', 'pendiente', 'Primera vez en el salón', 3000000),
(4, 3, 13, '2024-01-25 16:00:00', 'confirmada', 'Maquillaje para evento corporativo', 3500000),
(2, 1, 2, '2024-01-15 09:00:00', 'completada', 'Cambio a rubio', 4500000),
(3, 4, 5, '2024-01-18 11:00:00', 'completada', 'Peinado para boda', 4000000);
