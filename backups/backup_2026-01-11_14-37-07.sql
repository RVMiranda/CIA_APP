-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alumnos_alumno`
--

DROP TABLE IF EXISTS `alumnos_alumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumnos_alumno` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `matricula` varchar(12) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `edad` int unsigned DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `nombre_tutor` varchar(100) DEFAULT NULL,
  `telefono_tutor` varchar(15) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) DEFAULT NULL,
  `es_nuevo` tinyint(1) NOT NULL,
  `dia_pago_preferido` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `matricula` (`matricula`),
  CONSTRAINT `alumnos_alumno_chk_1` CHECK ((`edad` >= 0)),
  CONSTRAINT `alumnos_alumno_chk_2` CHECK ((`dia_pago_preferido` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnos_alumno`
--

LOCK TABLES `alumnos_alumno` WRITE;
/*!40000 ALTER TABLE `alumnos_alumno` DISABLE KEYS */;
INSERT INTO `alumnos_alumno` (`id`, `nombre`, `apellido`, `matricula`, `fecha_nacimiento`, `edad`, `telefono`, `nombre_tutor`, `telefono_tutor`, `direccion`, `activo`, `fecha_creacion`, `fecha_actualizacion`, `es_nuevo`, `dia_pago_preferido`) VALUES (1,'alondra','miranda','AM8636','2011-07-10',14,'9191502288','Valentin Miranda','9193218765','11a oriente sur barrio tonina',1,'2026-01-11 04:05:20.209163','2026-01-11 04:05:20.209178',0,15),(2,'Maricela','Cruz Lopez','MC0613','2003-04-01',23,'9191234567','Joaquin Hernandez','9196703514','colonia magisterial',1,'2026-01-11 20:14:19.536584','2026-01-11 20:14:19.536609',1,10);
/*!40000 ALTER TABLE `alumnos_alumno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnos_inscripcion`
--

DROP TABLE IF EXISTS `alumnos_inscripcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumnos_inscripcion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_inscripcion` date NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `alumno_id` bigint NOT NULL,
  `nivel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `alumnos_inscripcion_alumno_id_nivel_id_6295d047_uniq` (`alumno_id`,`nivel_id`),
  KEY `alumnos_inscripcion_nivel_id_ca9e189e_fk_alumnos_nivelingles_id` (`nivel_id`),
  CONSTRAINT `alumnos_inscripcion_alumno_id_eafb1fde_fk_alumnos_alumno_id` FOREIGN KEY (`alumno_id`) REFERENCES `alumnos_alumno` (`id`),
  CONSTRAINT `alumnos_inscripcion_nivel_id_ca9e189e_fk_alumnos_nivelingles_id` FOREIGN KEY (`nivel_id`) REFERENCES `alumnos_nivelingles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnos_inscripcion`
--

LOCK TABLES `alumnos_inscripcion` WRITE;
/*!40000 ALTER TABLE `alumnos_inscripcion` DISABLE KEYS */;
INSERT INTO `alumnos_inscripcion` (`id`, `fecha_inscripcion`, `monto`, `alumno_id`, `nivel_id`) VALUES (1,'2026-01-10',150.00,1,1),(2,'2026-01-11',200.00,2,1);
/*!40000 ALTER TABLE `alumnos_inscripcion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnos_nivelingles`
--

DROP TABLE IF EXISTS `alumnos_nivelingles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumnos_nivelingles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `sub_nivel` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `alumnos_nivelingles_nombre_sub_nivel_cec6f8ac_uniq` (`nombre`,`sub_nivel`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnos_nivelingles`
--

LOCK TABLES `alumnos_nivelingles` WRITE;
/*!40000 ALTER TABLE `alumnos_nivelingles` DISABLE KEYS */;
INSERT INTO `alumnos_nivelingles` (`id`, `nombre`, `sub_nivel`) VALUES (1,'Avanzado','C2');
/*!40000 ALTER TABLE `alumnos_nivelingles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnos_reinscripcion`
--

DROP TABLE IF EXISTS `alumnos_reinscripcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumnos_reinscripcion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_reinscripcion` date NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `alumno_id` bigint NOT NULL,
  `nivel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `alumnos_reinscripcion_alumno_id_nivel_id_b93c2dbe_uniq` (`alumno_id`,`nivel_id`),
  KEY `alumnos_reinscripcio_nivel_id_46221294_fk_alumnos_n` (`nivel_id`),
  CONSTRAINT `alumnos_reinscripcio_nivel_id_46221294_fk_alumnos_n` FOREIGN KEY (`nivel_id`) REFERENCES `alumnos_nivelingles` (`id`),
  CONSTRAINT `alumnos_reinscripcion_alumno_id_6167fc0a_fk_alumnos_alumno_id` FOREIGN KEY (`alumno_id`) REFERENCES `alumnos_alumno` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnos_reinscripcion`
--

LOCK TABLES `alumnos_reinscripcion` WRITE;
/*!40000 ALTER TABLE `alumnos_reinscripcion` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumnos_reinscripcion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Alumno',7,'add_alumno'),(26,'Can change Alumno',7,'change_alumno'),(27,'Can delete Alumno',7,'delete_alumno'),(28,'Can view Alumno',7,'view_alumno'),(29,'Can add Nivel de Ingles',8,'add_nivelingles'),(30,'Can change Nivel de Ingles',8,'change_nivelingles'),(31,'Can delete Nivel de Ingles',8,'delete_nivelingles'),(32,'Can view Nivel de Ingles',8,'view_nivelingles'),(33,'Can add Reinscripción',9,'add_reinscripcion'),(34,'Can change Reinscripción',9,'change_reinscripcion'),(35,'Can delete Reinscripción',9,'delete_reinscripcion'),(36,'Can view Reinscripción',9,'view_reinscripcion'),(37,'Can add Inscripción',10,'add_inscripcion'),(38,'Can change Inscripción',10,'change_inscripcion'),(39,'Can delete Inscripción',10,'delete_inscripcion'),(40,'Can view Inscripción',10,'view_inscripcion'),(41,'Can add Descuento',11,'add_descuento'),(42,'Can change Descuento',11,'change_descuento'),(43,'Can delete Descuento',11,'delete_descuento'),(44,'Can view Descuento',11,'view_descuento'),(45,'Can add Recargo',12,'add_recargo'),(46,'Can change Recargo',12,'change_recargo'),(47,'Can delete Recargo',12,'delete_recargo'),(48,'Can view Recargo',12,'view_recargo'),(49,'Can add Colegiatura',13,'add_colegiatura'),(50,'Can change Colegiatura',13,'change_colegiatura'),(51,'Can delete Colegiatura',13,'delete_colegiatura'),(52,'Can view Colegiatura',13,'view_colegiatura'),(53,'Can add Grupo',14,'add_grupo'),(54,'Can change Grupo',14,'change_grupo'),(55,'Can delete Grupo',14,'delete_grupo'),(56,'Can view Grupo',14,'view_grupo'),(57,'Can add Asignación de Grupo',15,'add_grupoalumno'),(58,'Can change Asignación de Grupo',15,'change_grupoalumno'),(59,'Can delete Asignación de Grupo',15,'delete_grupoalumno'),(60,'Can view Asignación de Grupo',15,'view_grupoalumno');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES (1,'pbkdf2_sha256$260000$H8FhI9Qg8ap2tou4wRnDIJ$g+dPWsnMzA/WwEwKsJ7rFdkzBFG3vVHWvSHqwRpIPq4=','2026-01-11 19:21:27.648022',1,'admin','','','admin@example.com',1,1,'2026-01-09 21:32:03.055371');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colegiaturas_colegiatura`
--

DROP TABLE IF EXISTS `colegiaturas_colegiatura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colegiaturas_colegiatura` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `anio` int NOT NULL,
  `mes` int NOT NULL,
  `fecha_pago` date DEFAULT NULL,
  `fecha_vencimiento` date NOT NULL,
  `monto_base` decimal(10,2) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `alumno_id` bigint NOT NULL,
  `descuento_aplicado` decimal(10,2) NOT NULL,
  `descuento_ref_id` bigint DEFAULT NULL,
  `estado_pago` varchar(20) NOT NULL,
  `monto_pagado` decimal(10,2) DEFAULT NULL,
  `recargo_aplicado` decimal(10,2) NOT NULL,
  `recargo_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `colegiaturas_colegiatura_alumno_id_anio_mes_08503f13_uniq` (`alumno_id`,`anio`,`mes`),
  KEY `colegiaturas_colegia_descuento_ref_id_9829a4c9_fk_colegiatu` (`descuento_ref_id`),
  KEY `colegiaturas_colegia_recargo_ref_id_4b75051d_fk_colegiatu` (`recargo_ref_id`),
  CONSTRAINT `colegiaturas_colegia_descuento_ref_id_9829a4c9_fk_colegiatu` FOREIGN KEY (`descuento_ref_id`) REFERENCES `colegiaturas_descuento` (`id`),
  CONSTRAINT `colegiaturas_colegia_recargo_ref_id_4b75051d_fk_colegiatu` FOREIGN KEY (`recargo_ref_id`) REFERENCES `colegiaturas_recargo` (`id`),
  CONSTRAINT `colegiaturas_colegiatura_alumno_id_3d7ac95d_fk_alumnos_alumno_id` FOREIGN KEY (`alumno_id`) REFERENCES `alumnos_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colegiaturas_colegiatura`
--

LOCK TABLES `colegiaturas_colegiatura` WRITE;
/*!40000 ALTER TABLE `colegiaturas_colegiatura` DISABLE KEYS */;
INSERT INTO `colegiaturas_colegiatura` (`id`, `anio`, `mes`, `fecha_pago`, `fecha_vencimiento`, `monto_base`, `fecha_registro`, `alumno_id`, `descuento_aplicado`, `descuento_ref_id`, `estado_pago`, `monto_pagado`, `recargo_aplicado`, `recargo_ref_id`) VALUES (1,2026,1,'2026-01-10','2026-01-15',650.00,'2026-01-11 04:05:20.219664',1,0.00,NULL,'Pagado',650.00,0.00,NULL),(2,2026,2,NULL,'2026-02-15',650.00,'2026-01-11 04:06:12.059838',1,0.00,NULL,'Pendiente',NULL,0.00,NULL),(3,2026,1,'2026-01-11','2026-01-10',700.00,'2026-01-11 20:14:19.563922',2,0.00,NULL,'Pagado',700.00,0.00,NULL),(4,2026,2,NULL,'2026-02-10',700.00,'2026-01-11 20:15:06.078771',2,0.00,NULL,'Pendiente',NULL,0.00,NULL);
/*!40000 ALTER TABLE `colegiaturas_colegiatura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colegiaturas_descuento`
--

DROP TABLE IF EXISTS `colegiaturas_descuento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colegiaturas_descuento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(255) NOT NULL,
  `meses_anticipo` int NOT NULL,
  `porcentaje` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `meses_anticipo` (`meses_anticipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colegiaturas_descuento`
--

LOCK TABLES `colegiaturas_descuento` WRITE;
/*!40000 ALTER TABLE `colegiaturas_descuento` DISABLE KEYS */;
/*!40000 ALTER TABLE `colegiaturas_descuento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colegiaturas_recargo`
--

DROP TABLE IF EXISTS `colegiaturas_recargo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colegiaturas_recargo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(255) NOT NULL,
  `porcentaje_por_dia` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colegiaturas_recargo`
--

LOCK TABLES `colegiaturas_recargo` WRITE;
/*!40000 ALTER TABLE `colegiaturas_recargo` DISABLE KEYS */;
/*!40000 ALTER TABLE `colegiaturas_recargo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES (1,'2026-01-11 04:05:08.506476','1','Avanzado - C2',1,'[{\"added\": {}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (1,'admin','logentry'),(7,'alumnos','alumno'),(10,'alumnos','inscripcion'),(8,'alumnos','nivelingles'),(9,'alumnos','reinscripcion'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(13,'colegiaturas','colegiatura'),(11,'colegiaturas','descuento'),(12,'colegiaturas','recargo'),(5,'contenttypes','contenttype'),(14,'grupos','grupo'),(15,'grupos','grupoalumno'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (1,'contenttypes','0001_initial','2026-01-09 21:22:18.594065'),(2,'auth','0001_initial','2026-01-09 21:22:19.160262'),(3,'admin','0001_initial','2026-01-09 21:22:19.300538'),(4,'admin','0002_logentry_remove_auto_add','2026-01-09 21:22:19.308947'),(5,'admin','0003_logentry_add_action_flag_choices','2026-01-09 21:22:19.316058'),(6,'alumnos','0001_initial','2026-01-09 21:22:19.655287'),(7,'alumnos','0002_alumno_es_nuevo','2026-01-09 21:22:19.713068'),(8,'alumnos','0003_alumno_dia_pago_preferido','2026-01-09 21:22:19.781584'),(9,'contenttypes','0002_remove_content_type_name','2026-01-09 21:22:19.879292'),(10,'auth','0002_alter_permission_name_max_length','2026-01-09 21:22:19.943301'),(11,'auth','0003_alter_user_email_max_length','2026-01-09 21:22:19.961031'),(12,'auth','0004_alter_user_username_opts','2026-01-09 21:22:19.968456'),(13,'auth','0005_alter_user_last_login_null','2026-01-09 21:22:20.014968'),(14,'auth','0006_require_contenttypes_0002','2026-01-09 21:22:20.018706'),(15,'auth','0007_alter_validators_add_error_messages','2026-01-09 21:22:20.028831'),(16,'auth','0008_alter_user_username_max_length','2026-01-09 21:22:20.093940'),(17,'auth','0009_alter_user_last_name_max_length','2026-01-09 21:22:20.152654'),(18,'auth','0010_alter_group_name_max_length','2026-01-09 21:22:20.168305'),(19,'auth','0011_update_proxy_permissions','2026-01-09 21:22:20.179761'),(20,'auth','0012_alter_user_first_name_max_length','2026-01-09 21:22:20.238983'),(21,'colegiaturas','0001_initial','2026-01-09 21:22:20.515250'),(22,'colegiaturas','0002_auto_20250723_2022','2026-01-09 21:22:21.049586'),(23,'grupos','0001_initial','2026-01-09 21:22:21.275705'),(24,'sessions','0001_initial','2026-01-09 21:22:21.313706');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES ('4vb01ocd8dyeunickb7oj49mkpu2ervb','.eJxVjEEOwiAQRe_C2pBSyAAu3XsGMswMUjU0Ke3KeHdt0oVu_3vvv1TCba1p67KkidVZGXX63TLSQ9oO-I7tNmua27pMWe-KPmjX15nleTncv4OKvX7r6MAZAhJGpDz66ELGwhktGGdQsicOhQoN1kM0ASiAsSzDyBZcIfX-AAsJOMA:1veKBX:c34H_q7s9q42kAXUKhYZHRne3DBYDe9LNoJC6pLGeag','2026-01-09 23:38:19.518710'),('r62wngybc42xjtk4tnrat1c7ni7wai6e','.eJxVjEEOwiAQRe_C2pBSyAAu3XsGMswMUjU0Ke3KeHdt0oVu_3vvv1TCba1p67KkidVZGXX63TLSQ9oO-I7tNmua27pMWe-KPmjX15nleTncv4OKvX7r6MAZAhJGpDz66ELGwhktGGdQsicOhQoN1kM0ASiAsSzDyBZcIfX-AAsJOMA:1vemfD:_UtSVwfLxMkqIuwjVByvMWgG3Lhki0t0ZEGC5M9bXBA','2026-01-11 06:02:51.998624'),('x91xyq9o5ougtrhowfeix45j064hfu08','.eJxVjEEOwiAQRe_C2pBSyAAu3XsGMswMUjU0Ke3KeHdt0oVu_3vvv1TCba1p67KkidVZGXX63TLSQ9oO-I7tNmua27pMWe-KPmjX15nleTncv4OKvX7r6MAZAhJGpDz66ELGwhktGGdQsicOhQoN1kM0ASiAsSzDyBZcIfX-AAsJOMA:1vf10B:8dE8QSbRfTYSsgP0z8L6yiGyZiRLP_QRqArx9O0Sc1Y','2026-01-11 21:21:27.669191');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos_grupo`
--

DROP TABLE IF EXISTS `grupos_grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos_grupo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `nivel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grupos_grupo_nombre_nivel_id_0e9e9afc_uniq` (`nombre`,`nivel_id`),
  KEY `grupos_grupo_nivel_id_e1158b9d_fk_alumnos_nivelingles_id` (`nivel_id`),
  CONSTRAINT `grupos_grupo_nivel_id_e1158b9d_fk_alumnos_nivelingles_id` FOREIGN KEY (`nivel_id`) REFERENCES `alumnos_nivelingles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos_grupo`
--

LOCK TABLES `grupos_grupo` WRITE;
/*!40000 ALTER TABLE `grupos_grupo` DISABLE KEYS */;
/*!40000 ALTER TABLE `grupos_grupo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos_grupoalumno`
--

DROP TABLE IF EXISTS `grupos_grupoalumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos_grupoalumno` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_asignacion` date NOT NULL,
  `alumno_id` bigint NOT NULL,
  `grupo_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grupos_grupoalumno_alumno_id_grupo_id_fd84c6a8_uniq` (`alumno_id`,`grupo_id`),
  KEY `grupos_grupoalumno_grupo_id_de0817e3_fk_grupos_grupo_id` (`grupo_id`),
  CONSTRAINT `grupos_grupoalumno_alumno_id_0206522b_fk_alumnos_alumno_id` FOREIGN KEY (`alumno_id`) REFERENCES `alumnos_alumno` (`id`),
  CONSTRAINT `grupos_grupoalumno_grupo_id_de0817e3_fk_grupos_grupo_id` FOREIGN KEY (`grupo_id`) REFERENCES `grupos_grupo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos_grupoalumno`
--

LOCK TABLES `grupos_grupoalumno` WRITE;
/*!40000 ALTER TABLE `grupos_grupoalumno` DISABLE KEYS */;
/*!40000 ALTER TABLE `grupos_grupoalumno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'mydb'
--

--
-- Dumping routines for database 'mydb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-11 20:37:08
