-- 1. Insertar Especialidades (5 registros)
INSERT INTO especialidades (nombre, descripcion) VALUES
('Medicina General', 'Atención primaria y diagnóstico básico'),
('Pediatría', 'Atención médica integral para recién nacidos, niños y adolescentes'),
('Cardiología', 'Estudio, diagnóstico y tratamiento de enfermedades del corazón'),
('Dermatología', 'Tratamiento de enfermedades de la piel, cabello y uñas'),
('Ortopedia', 'Tratamiento de afecciones del sistema musculoesquelético');

-- 2. Insertar Médicos (5 registros)
INSERT INTO medicos (nombre, apellido, documento, telefono, correo) VALUES
('Carlos', 'Restrepo', '1098765432', '3101234567', 'crestrepo@consultorio.com.co'),
('María', 'Jaramillo', '1098123456', '3119876543', 'mjaramillo@consultorio.com.co'),
('Luis', 'Pérez', '1357924680', '3205554433', 'lperez@consultorio.com.co'),
('Andrea', 'Gómez', '1122334455', '3156667788', 'agomez@consultorio.com.co'),
('Jorge', 'Velandia', '1098555666', '3001112233', 'jvelandia@consultorio.com.co');

-- 3. Asignar Especialidades a los Médicos (Tabla Intermedia N:M)
INSERT INTO medico_especialidad (id_medico, id_especialidad) VALUES
(1, 1), (1, 2), -- Dr. Carlos: Medicina General y Pediatría
(2, 3),         -- Dra. María: Cardiología
(3, 4),         -- Dr. Luis: Dermatología
(4, 1),         -- Dra. Andrea: Medicina General
(5, 5);         -- Dr. Jorge: Ortopedia

-- 4. Insertar Pacientes (11 registros - Contexto Colombia)
INSERT INTO pacientes (nombre, apellido, documento, fecha_nacimiento, telefono, correo, direccion) VALUES
('Juan', 'Cárdenas', '1001112223', '1990-05-15', '3009998877', 'jcardenas@gmail.com', 'Cra 27 # 36-14, Bucaramanga'),
('Laura', 'Ríos', '1002223334', '1985-08-22', '3108887766', 'lrios@hotmail.com', 'Calle 56 # 12-45, Bucaramanga'),
('Pedro', 'Flórez', '1003334445', '1978-11-03', '3207776655', 'pflorez@outlook.com', 'Cra 33 # 45-20, Bucaramanga'),
('Ana', 'Osorio', '1004445556', '1995-02-10', '3156665544', 'aosorio@gmail.com', 'Barrio Cabecera, Bucaramanga'),
('Diego', 'Mendoza', '1005556667', '2000-09-30', '3165554433', 'dmendoza@yahoo.com', 'Calle 20 # 15-10, Floridablanca'),
('Valentina', 'Rojas', '1006667778', '1992-04-18', '3174443322', 'vrojas@gmail.com', 'Cra 15 # 22-05, Piedecuesta'),
('Andrés', 'Silva', '1007778889', '1982-12-05', '3183332211', 'asilva@hotmail.com', 'Barrio San Francisco, Bucaramanga'),
('Camila', 'Gutiérrez', '1008889990', '1998-07-25', '3192221100', 'cgutierrez@gmail.com', 'Calle 10 # 5-50, Girón'),
('Felipe', 'Morales', '1009990001', '1975-01-12', '3211110099', 'fmorales@outlook.com', 'Cra 9 # 4-25, Bucaramanga'),
('Isabella', 'Navarro', '1010001112', '2005-06-08', '3220009988', 'inavarro@gmail.com', 'Barrio Provenza, Bucaramanga'),
('Mateo', 'Quintero', '1011112223', '2010-03-14', '3001239876', 'mquintero@gmail.com', 'Calle 45 # 29-10, Bucaramanga');

-- 5. Insertar Horarios de Atención Básicos
INSERT INTO horarios (id_medico, dia_semana, hora_inicio, hora_fin) VALUES
(1, 1, '08:00', '12:00'), (1, 2, '08:00', '12:00'), (1, 3, '08:00', '12:00'),
(2, 3, '14:00', '18:00'), (2, 4, '14:00', '18:00'),
(3, 1, '14:00', '18:00'), (3, 5, '08:00', '12:00'),
(4, 2, '08:00', '16:00'), (4, 4, '08:00', '16:00'),
(5, 5, '08:00', '18:00');

-- 6. Insertar Citas (Total: 25 citas - 15 Atendidas, 5 Canceladas, 5 Programadas)
-- Citas ATENDIDAS (1 a 15)
INSERT INTO citas (id_paciente, id_medico, fecha, hora, estado, motivo) VALUES
(1, 1, '2025-10-01', '08:30:00', 'atendida', 'Dolor de cabeza constante'),
(2, 2, '2025-10-02', '14:30:00', 'atendida', 'Palpitaciones y fatiga'),
(3, 3, '2025-10-03', '15:00:00', 'atendida', 'Manchas rojas en la piel'),
(4, 4, '2025-10-04', '09:00:00', 'atendida', 'Fiebre y malestar general'),
(5, 5, '2025-10-05', '09:30:00', 'atendida', 'Dolor en la rodilla derecha'),
(6, 1, '2025-10-06', '10:00:00', 'atendida', 'Control general anual'),
(7, 2, '2025-10-07', '15:30:00', 'atendida', 'Control de presión arterial'),
(8, 3, '2025-10-08', '08:30:00', 'atendida', 'Brote severo de acné'),
(9, 4, '2025-10-09', '14:30:00', 'atendida', 'Dolor de garganta agudo'),
(10, 5, '2025-10-10', '10:00:00', 'atendida', 'Torcedura de tobillo'),
(11, 1, '2025-10-11', '08:00:00', 'atendida', 'Control de crecimiento pediátrico'),
(1, 2, '2025-10-12', '16:00:00', 'atendida', 'Chequeo preventivo de rutina'),
(2, 3, '2025-10-13', '11:30:00', 'atendida', 'Revisión de lunares sospechosos'),
(3, 4, '2025-10-14', '14:30:00', 'atendida', 'Síntomas sospechosos de dengue'),
(4, 5, '2025-10-15', '11:00:00', 'atendida', 'Dolor lumbar crónico'),
-- Citas CANCELADAS (16 a 20)
(5, 1, '2025-11-01', '09:00:00', 'cancelada', 'Paciente de viaje'),
(6, 2, '2025-11-02', '15:00:00', 'cancelada', 'Imposibilidad de asistir'),
(7, 3, '2025-11-03', '10:00:00', 'cancelada', 'Reprogramada por EPS'),
(8, 4, '2025-11-04', '14:00:00', 'cancelada', 'Inconveniente de transporte'),
(9, 5, '2025-11-05', '16:00:00', 'cancelada', 'No informa motivo'),
-- Citas PROGRAMADAS (21 a 25) - Fechas en el futuro
(10, 1, '2026-08-15', '08:30:00', 'programada', 'Revisión de resultados de laboratorio'),
(11, 2, '2026-08-16', '14:30:00', 'programada', 'Electrocardiograma de control'),
(1, 3, '2026-08-17', '15:00:00', 'programada', 'Consulta por dermatitis atópica'),
(2, 4, '2026-08-18', '10:00:00', 'programada', 'Lectura de exámenes de sangre'),
(3, 5, '2026-08-19', '11:30:00', 'programada', 'Control post-operatorio de meniscos');

-- 7. Insertar Consultas Médicas (Total: 15 - Enlazadas a las citas atendidas 1-15)
INSERT INTO consultas (id_cita, diagnostico, observaciones) VALUES
(1, 'Migraña tensional leve', 'El paciente refiere altos niveles de estrés laboral. Se recomienda pausas activas.'),
(2, 'Arritmia leve', 'Se solicita examen Holter de 24 horas para descartar patologías mayores.'),
(3, 'Dermatitis por contacto', 'Reacción alérgica probable a un nuevo jabón o detergente. Evitar irritantes.'),
(4, 'Faringoamigdalitis viral', 'Cuadro viral agudo, no se observan placas de pus. No requiere antibióticos por el momento.'),
(5, 'Tendinitis rotuliana', 'Inflamación por esfuerzo excesivo jugando microfútbol.'),
(6, 'Paciente sano', 'Examen físico general dentro de los límites normales, sin hallazgos patológicos.'),
(7, 'Hipertensión arterial estadio 1', 'Se inician cambios en estilo de vida y monitoreo diario de presión arterial.'),
(8, 'Acné vulgar grado 2', 'Paciente requiere tratamiento tópico continuo y evitar alimentos grasos.'),
(9, 'Amigdalitis estreptocócica', 'Presencia de placas purulentas en amígdalas, requiere manejo antibiótico urgente.'),
(10, 'Esguince de tobillo grado 1', 'Sin ruptura de ligamentos. Reposo relativo y elevación de la extremidad.'),
(11, 'Desarrollo psicomotor adecuado', 'Percentiles de talla y peso en rango normal para la edad en población colombiana.'),
(12, 'Examen cardiovascular normal', 'Riesgo cardiovascular muy bajo, continuar con buenos hábitos deportivos.'),
(13, 'Nevus melanocítico benigno', 'Lunar asimétrico pero sin signos de malignidad actual. Control en 12 meses.'),
(14, 'Dengue clásico (Sin signos de alarma)', 'Prueba rápida NS1 positiva. Manejo sintomático en casa, alarma ante sangrados.'),
(15, 'Lumbalgia mecánica', 'Espasmo muscular severo por mala higiene postural en puesto de trabajo.');

-- 8. Insertar Tratamientos y Medicamentos (Enlazados a las 15 consultas)
INSERT INTO tratamientos (id_consulta, medicamento) VALUES
(1, 'Ibuprofeno 400mg cada 8 horas por 3 días. Pausas activas cada hora.'),
(2, 'Ningún medicamento por ahora. Esperar resultados de electrocardiograma y Holter.'),
(3, 'Crema tópica con Hidrocortisona al 1% aplicar capa fina cada 12 horas por 5 días.'),
(4, 'Acetaminofén 500mg cada 6 horas para control de fiebre. Abundantes líquidos.'),
(5, 'Naproxeno 250mg cada 12 horas. Remisión a fisioterapia (5 sesiones).'),
(6, 'Ninguno. Continuar con dieta balanceada y ejercicio regular de 30 min diarios.'),
(7, 'Losartán 50mg (1 tableta al día). Dieta hiposódica estricta.'),
(8, 'Peróxido de benzoilo al 5% en gel. Aplicar solo en las noches.'),
(9, 'Amoxicilina 500mg cada 8 horas por 7 días exactos. No suspender tratamiento.'),
(10, 'Diclofenaco en gel aplicar 3 veces al día. Uso de vendaje elástico compresivo.'),
(11, 'Suplemento vitamínico diario (opcional).'),
(12, 'Ninguno. Próximo control en un año.'),
(13, 'Protector solar dermatológico FPS 50+, uso diario y retocar cada 4 horas.'),
(14, 'Suero oral a demanda. Acetaminofén 500mg si hay fiebre. ESTRICTAMENTE PROHIBIDO EL USO DE AINES.'),
(15, 'Metocarbamol 750mg cada 8 horas por 3 días. Uso de cojín ergonómico.');