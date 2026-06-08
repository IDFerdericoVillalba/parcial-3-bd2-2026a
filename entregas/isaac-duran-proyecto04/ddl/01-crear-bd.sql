-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema consultorio_medico
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema consultorio_medico
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `consultorio_medico` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `consultorio_medico` ;

-- -----------------------------------------------------
-- Table `consultorio_medico`.`medicos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`medicos` (
  `id_medico` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `apellido` VARCHAR(80) NOT NULL,
  `documento` VARCHAR(20) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_medico`),
  UNIQUE INDEX `uq_medico_registro` (`documento` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `consultorio_medico`.`pacientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`pacientes` (
  `id_paciente` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `apellido` VARCHAR(80) NOT NULL,
  `documento` VARCHAR(20) NOT NULL,
  `fecha_nacimiento` DATE NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `correo` VARCHAR(100) NULL DEFAULT NULL,
  `direccion` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`id_paciente`),
  UNIQUE INDEX `uq_pac_documento` (`documento` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `consultorio_medico`.`citas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`citas` (
  `id_cita` INT NOT NULL AUTO_INCREMENT,
  `id_paciente` INT NOT NULL,
  `id_medico` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `hora` TIME NOT NULL,
  `estado` ENUM('programada', 'atendida', 'cancelada', 'no_asistio') NOT NULL DEFAULT 'programada',
  `motivo` TEXT NOT NULL,
  PRIMARY KEY (`id_cita`),
  INDEX `fk_cita_paciente1_idx` (`id_paciente` ASC) VISIBLE,
  INDEX `fk_cita_medico1_idx` (`id_medico` ASC) VISIBLE,
  CONSTRAINT `fk_cita_medico1`
    FOREIGN KEY (`id_medico`)
    REFERENCES `consultorio_medico`.`medicos` (`id_medico`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_cita_paciente1`
    FOREIGN KEY (`id_paciente`)
    REFERENCES `consultorio_medico`.`pacientes` (`id_paciente`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `consultorio_medico`.`consultas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`consultas` (
  `id_consulta` INT NOT NULL AUTO_INCREMENT,
  `id_cita` INT NOT NULL,
  `diagnostico` TEXT NOT NULL,
  `observaciones` TEXT NULL DEFAULT NULL,
  `fecha_registro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_consulta`),
  INDEX `fk_consulta_cita1_idx` (`id_cita` ASC) VISIBLE,
  CONSTRAINT `fk_consulta_cita1`
    FOREIGN KEY (`id_cita`)
    REFERENCES `consultorio_medico`.`citas` (`id_cita`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `consultorio_medico`.`especialidades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`especialidades` (
  `id_especialidad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_especialidad`),
  UNIQUE INDEX `uq_esp_nombre` (`nombre` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `consultorio_medico`.`horarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`horarios` (
  `id_horario` INT NOT NULL AUTO_INCREMENT,
  `id_medico` INT NOT NULL,
  `dia_semana` TINYINT NOT NULL COMMENT '1=Lunes, 7=Domingo',
  `hora_inicio` TIME NOT NULL,
  `hora_fin` TIME NOT NULL,
  PRIMARY KEY (`id_horario`),
  UNIQUE INDEX `uq_horario_medico` (`id_medico` ASC, `dia_semana` ASC, `hora_inicio` ASC) INVISIBLE,
  INDEX `fk_horarios_medico1_idx` (`id_medico` ASC) INVISIBLE,
  CONSTRAINT `fk_horarios_medico1`
    FOREIGN KEY (`id_medico`)
    REFERENCES `consultorio_medico`.`medicos` (`id_medico`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `consultorio_medico`.`medico_especialidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`medico_especialidad` (
  `id_medico` INT NOT NULL,
  `id_especialidad` INT NOT NULL,
  PRIMARY KEY (`id_medico`, `id_especialidad`),
  INDEX `fk_mesp_esp_idx` (`id_especialidad` ASC) VISIBLE,
  CONSTRAINT `fk_mesp_esp`
    FOREIGN KEY (`id_especialidad`)
    REFERENCES `consultorio_medico`.`especialidades` (`id_especialidad`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_mesp_medico`
    FOREIGN KEY (`id_medico`)
    REFERENCES `consultorio_medico`.`medicos` (`id_medico`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `consultorio_medico`.`tratamientos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `consultorio_medico`.`tratamientos` (
  `id_tratamiento` INT NOT NULL AUTO_INCREMENT,
  `id_consulta` INT NOT NULL,
  `medicamento` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id_tratamiento`),
  INDEX `fk_tratamiento_consulta1_idx` (`id_consulta` ASC) VISIBLE,
  CONSTRAINT `fk_tratamiento_consulta1`
    FOREIGN KEY (`id_consulta`)
    REFERENCES `consultorio_medico`.`consultas` (`id_consulta`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;