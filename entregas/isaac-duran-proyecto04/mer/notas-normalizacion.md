

1. Primera Forma Normal (1FN) - Atomicidad
Se garantizó que todos los atributos de las tablas sean atómicos (indivisibles) y se eliminaron los grupos repetitivos.
* **Separación de nombres:** En las tablas `pacientes` y `medicos`, los campos `nombre` y `apellido` están separados, evitando campos compuestos que dificulten las búsquedas.
* **Grupos repetitivos eliminados:** En la tabla `horarios`, en lugar de almacenar los días de atención en un solo campo de texto (ej. `"Lunes, Martes"`), se diseñó la tabla para que cada bloque de tiempo en un día específico (`dia_semana`, `hora_inicio`, `hora_fin`) sea una fila individual. 
* **Tratamientos independientes:** Un paciente puede recibir múltiples medicamentos en una sola consulta. Para mantener la atomicidad, se creó la tabla `tratamientos` donde cada medicamento formulado es un registro único enlazado al `id_consulta`.


2. Segunda Forma Normal (2FN) - Dependencia Completa de la Llave Primaria
Todas las tablas cumplen con la 1FN y se aseguró que los atributos no clave dependan de la totalidad de la llave primaria.
* **Resolución de la relación Muchos a Muchos (N:M):** Un médico puede tener varias especialidades y una especialidad pertenece a varios médicos. Para cumplir con la 2FN, se implementó la tabla intermedia `medico_especialidad`.
* **Llave compuesta:** La llave primaria de esta tabla intermedia es compuesta (`id_medico`, `id_especialidad`). No existen atributos adicionales en esta tabla que dependan solo del médico o solo de la especialidad, cumpliendo así con la dependencia completa.


3. Tercera Forma Normal (3FN) - Cero Dependencias Transitivas
Todas las tablas cumplen con la 2FN y ningún atributo no clave depende de otro atributo no clave.
* **Tabla Citas:** Al programar una atención, la tabla `citas` solo almacena las llaves foráneas (`id_paciente`, `id_medico`) junto con los datos propios de la cita (`fecha`, `hora`, `estado`, `motivo`). No se almacena el nombre del paciente, ni el nombre del médico, ni su teléfono. Cualquier cambio en los datos de contacto del paciente se hace en su tabla maestra y se refleja automáticamente sin generar inconsistencias.
* **Tabla Consultas:** Se separó lógicamente la "Cita" (el evento programado) de la "Consulta" (el acto médico realizado). La tabla `consultas` solo almacena el `id_cita` para heredar el contexto, añadiendo el `diagnostico` y las `observaciones` generadas ese día.