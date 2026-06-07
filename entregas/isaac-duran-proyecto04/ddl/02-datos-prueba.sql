-- ==============================================================================
-- SCRIPT DML: POBLACIÓN DE DATOS DE PRUEBA (CUMPLIMIENTO DE RÚBRICA)
-- Base de Datos: consultorio_medico
-- ==============================================================================

USE `consultorio_medico`;

-- 1. Insertar Especialidades (Cumple regla: Mínimo 4)
INSERT INTO especialidades (nombre, descripcion) VALUES
('Medicina General', 'Atención primaria y valoración inicial del paciente.'),
('Cardiología', 'Estudio, diagnóstico y tratamiento de enfermedades del corazón.'),
('Pediatría', 'Atención médica integral para recién nacidos, niños y adolescentes.'),
('Dermatología', 'Tratamiento de enfermedades de la piel, cabello y uñas.'),
('Ortopedia', 'Tratamiento de afecciones del sistema musculoesquelético.');

-- 2. Insertar Médicos (Cumple regla: Mínimo 5)
INSERT INTO medicos (nombre, apellido, documento, telefono, correo) VALUES
('Carlos', 'Restrepo', '1098765432', '3101234567', 'crestrepo@consultorio.com'),
('María', 'Jaramillo', '1098123456', '3119876543', 'mjaramillo@consultorio.com'),
('Luis', 'Pérez', '1357924680', '3205554433', 'lperez@consultorio.com'),
('Andrea', 'Gómez', '1122334455', '3156667788', 'agomez@consultorio.com'),
('Jorge', 'Velandia', '1098555666', '3001112233', 'jvelandia@consultorio.com');

-- 3. Asignar Especialidades a los Médicos (Tabla Intermedia)
-- Nota Arquitectónica: Un médico puede tener múltiples especialidades.
INSERT INTO medico_especialidad (id_medico, id_especialidad) VALUES
(1, 1), (1, 3), -- Dr. Carlos (1): Medicina General y Pediatría
(2, 2),         -- Dra. María (2): Cardiología
(3, 4),         -- Dr. Luis (3): Dermatología
(4, 1),         -- Dra. Andrea (4): Medicina General
(5, 5);         -- Dr. Jorge (5): Ortopedia

-- 4. Insertar Pacientes (Cumple regla: Mínimo 10)
INSERT INTO pacientes (nombre, apellido, documento, fecha_nacimiento, telefono, correo, direccion) VALUES
('Juan', 'Cárdenas', '1001112223', '1990-05-15', '3009998877', 'jcardenas@mail.com', 'Cra 27 # 36-14'),
('Laura', 'Ríos', '1002223334', '1985-08-22', '3108887766', 'lrios@mail.com', 'Calle 56 # 12-45'),
('Pedro', 'Flórez', '1003334445', '1978-11-03', '3207776655', 'pflorez@mail.com', 'Cra 33 # 45-20'),
('Ana', 'Osorio', '1004445556', '1995-02-10', '3156665544', 'aosorio@mail.com', 'Barrio Cabecera'),
('Diego', 'Mendoza', '1005556667', '2000-09-30', '3165554433', 'dmendoza@mail.com', 'Calle 20 # 15-10'),
('Valentina', 'Rojas', '1006667778', '1992-04-18', '3174443322', 'vrojas@mail.com', 'Cra 15 # 22-05'),
('Andrés', 'Silva', '1007778889', '1982-12-05', '3183332211', 'asilva@mail.com', 'Barrio San Francisco'),
('Camila', 'Gutiérrez', '1008889990', '1998-07-25', '3192221100', 'cgutierrez@mail.com', 'Calle 10 # 5-50'),
('Felipe', 'Morales', '1009990001', '1975-01-12', '3211110099', 'fmorales@mail.com', 'Cra 9 # 4-25'),
('Isabella', 'Navarro', '1010001112', '2005-06-08', '3220009988', 'inavarro@mail.com', 'Barrio Provenza');

-- 5. Insertar Horarios de Atención Básicos
-- 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes
INSERT INTO horarios (id_medico, dia_semana, hora_inicio, hora_fin) VALUES
(1, 1, '08:00', '12:00'), (1, 2, '08:00', '12:00'), (1, 3, '08:00', '12:00'),
(2, 3, '14:00', '18:00'), (2, 4, '14:00', '18:00'),
(3, 1, '14:00', '18:00'), (3, 5, '08:00', '12:00'),
(4, 2, '08:00', '16:00'), (4, 4, '08:00', '16:00'),
(5, 5, '08:00', '18:00');

-- 6. Insertar Citas (Cumple regla: Mínimo 25 en distintos estados)
-- Citas ATENDIDAS (IDs 1 al 15)
INSERT INTO citas (id_paciente, id_medico, fecha, hora, estado, motivo) VALUES
(1, 1, '2023-10-01', '08:30:00', 'atendida', 'Dolor de cabeza constante'),
(2, 2, '2023-10-02', '14:30:00', 'atendida', 'Palpitaciones y fatiga'),
(3, 3, '2023-10-03', '15:00:00', 'atendida', 'Manchas rojas en la piel'),
(4, 4, '2023-10-04', '09:00:00', 'atendida', 'Fiebre y malestar general'),
(5, 5, '2023-10-05', '09:30:00', 'atendida', 'Dolor en la rodilla derecha'),
(6, 1, '2023-10-06', '10:00:00', 'atendida', 'Control general anual'),
(7, 2, '2023-10-07', '15:30:00', 'atendida', 'Control de presión arterial'),
(8, 3, '2023-10-08', '08:30:00', 'atendida', 'Brote severo de acné'),
(9, 4, '2023-10-09', '14:30:00', 'atendida', 'Dolor de garganta agudo'),
(10, 5, '2023-10-10', '10:00:00', 'atendida', 'Torcedura de tobillo'),
(1, 1, '2023-10-11', '08:00:00', 'atendida', 'Control de rutina general'),
(2, 2, '2023-10-12', '16:00:00', 'atendida', 'Chequeo preventivo de rutina'),
(3, 3, '2023-10-13', '11:30:00', 'atendida', 'Revisión de lunares sospechosos'),
(4, 4, '2023-10-14', '14:30:00', 'atendida', 'Síntomas sospechosos de dengue'),
(5, 5, '2023-10-15', '11:00:00', 'atendida', 'Dolor lumbar crónico'),
-- Citas CANCELADAS Y NO_ASISTIO (IDs 16 al 20)
(6, 1, '2023-11-01', '09:00:00', 'cancelada', 'Paciente de viaje'),
(7, 2, '2023-11-02', '15:00:00', 'no_asistio', 'Imposibilidad de asistir'),
(8, 3, '2023-11-03', '10:00:00', 'cancelada', 'Reprogramada por EPS'),
(9, 4, '2023-11-04', '14:00:00', 'no_asistio', 'Olvido de la cita'),
(10, 5, '2023-11-05', '16:00:00', 'cancelada', 'No informa motivo'),
-- Citas PROGRAMADAS (IDs 21 al 25)
(1, 1, '2026-12-15', '08:30:00', 'programada', 'Revisión de resultados de laboratorio'),
(2, 2, '2026-12-16', '14:30:00', 'programada', 'Electrocardiograma de control'),
(3, 3, '2026-12-17', '15:00:00', 'programada', 'Consulta por dermatitis atópica'),
(4, 4, '2026-12-18', '10:00:00', 'programada', 'Lectura de exámenes de sangre'),
(5, 5, '2026-12-19', '11:30:00', 'programada', 'Control post-operatorio de meniscos');

-- 7. Insertar Consultas Médicas (Cumple regla: Mínimo 15 registradas)
-- IMPORTANTE: Solo se asocian a las 15 citas que están marcadas como 'atendida' (IDs 1 al 15)
INSERT INTO consultas (id_cita, diagnostico, observaciones) VALUES
(1, 'Migraña tensional leve', 'El paciente refiere altos niveles de estrés laboral. Se recomienda descanso.'),
(2, 'Arritmia leve', 'Se solicita examen Holter de 24 horas para descartar patologías mayores.'),
(3, 'Dermatitis por contacto', 'Reacción alérgica probable a un nuevo jabón o detergente. Evitar irritantes.'),
(4, 'Faringoamigdalitis viral', 'Cuadro viral agudo. No requiere antibióticos por el momento.'),
(5, 'Tendinitis rotuliana', 'Inflamación por esfuerzo físico. Reposo deportivo.'),
(6, 'Paciente sano', 'Examen físico general dentro de los límites normales.'),
(7, 'Hipertensión arterial estadio 1', 'Se inician cambios en estilo de vida y monitoreo diario.'),
(8, 'Acné vulgar grado 2', 'Paciente requiere tratamiento tópico continuo.'),
(9, 'Amigdalitis estreptocócica', 'Presencia de placas. Requiere manejo antibiótico.'),
(10, 'Esguince de tobillo grado 1', 'Sin ruptura de ligamentos. Reposo relativo.'),
(11, 'Salud general óptima', 'Resultados de laboratorio normales.'),
(12, 'Examen cardiovascular normal', 'Riesgo cardiovascular muy bajo.'),
(13, 'Nevus melanocítico benigno', 'Lunar sin signos de malignidad actual. Control en 12 meses.'),
(14, 'Dengue clásico', 'Manejo sintomático en casa, alarma ante sangrados.'),
(15, 'Lumbalgia mecánica', 'Espasmo muscular severo por mala higiene postural.');

-- 8. Insertar Tratamientos y Medicamentos 
INSERT INTO tratamientos (id_consulta, medicamento) VALUES
(1, 'Ibuprofeno 400mg cada 8 horas por 3 días.'),
(2, 'Ningún medicamento por ahora. Esperar examen.'),
(3, 'Crema de Hidrocortisona al 1% cada 12 horas.'),
(4, 'Acetaminofén 500mg cada 6 horas para fiebre.'),
(5, 'Naproxeno 250mg cada 12 horas. Remisión a fisioterapia.'),
(6, 'Dieta balanceada y ejercicio regular.'),
(7, 'Losartán 50mg al día. Dieta hiposódica.'),
(8, 'Peróxido de benzoilo al 5% en gel.'),
(9, 'Amoxicilina 500mg cada 8 horas por 7 días.'),
(10, 'Diclofenaco en gel 3 veces al día. Vendaje elástico.'),
(11, 'Suplemento vitamínico diario.'),
(12, 'Ninguno. Próximo control en un año.'),
(13, 'Protector solar FPS 50+ uso diario.'),
(14, 'Suero oral a demanda. Acetaminofén 500mg.'),
(15, 'Metocarbamol 750mg cada 8 horas por 3 días.');