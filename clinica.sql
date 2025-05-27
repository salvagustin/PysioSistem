-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 26, 2025 at 05:03 AM
-- Server version: 11.6.2-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clinica`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add paciente', 1, 'add_paciente'),
(2, 'Can change paciente', 1, 'change_paciente'),
(3, 'Can delete paciente', 1, 'delete_paciente'),
(4, 'Can view paciente', 1, 'view_paciente'),
(5, 'Can add consulta', 2, 'add_consulta'),
(6, 'Can change consulta', 2, 'change_consulta'),
(7, 'Can delete consulta', 2, 'delete_consulta'),
(8, 'Can view consulta', 2, 'view_consulta'),
(9, 'Can add cita', 3, 'add_cita'),
(10, 'Can change cita', 3, 'change_cita'),
(11, 'Can delete cita', 3, 'delete_cita'),
(12, 'Can view cita', 3, 'view_cita'),
(13, 'Can add log entry', 4, 'add_logentry'),
(14, 'Can change log entry', 4, 'change_logentry'),
(15, 'Can delete log entry', 4, 'delete_logentry'),
(16, 'Can view log entry', 4, 'view_logentry'),
(17, 'Can add permission', 5, 'add_permission'),
(18, 'Can change permission', 5, 'change_permission'),
(19, 'Can delete permission', 5, 'delete_permission'),
(20, 'Can view permission', 5, 'view_permission'),
(21, 'Can add group', 6, 'add_group'),
(22, 'Can change group', 6, 'change_group'),
(23, 'Can delete group', 6, 'delete_group'),
(24, 'Can view group', 6, 'view_group'),
(25, 'Can add user', 7, 'add_user'),
(26, 'Can change user', 7, 'change_user'),
(27, 'Can delete user', 7, 'delete_user'),
(28, 'Can view user', 7, 'view_user'),
(29, 'Can add content type', 8, 'add_contenttype'),
(30, 'Can change content type', 8, 'change_contenttype'),
(31, 'Can delete content type', 8, 'delete_contenttype'),
(32, 'Can view content type', 8, 'view_contenttype'),
(33, 'Can add session', 9, 'add_session'),
(34, 'Can change session', 9, 'change_session'),
(35, 'Can delete session', 9, 'delete_session'),
(36, 'Can view session', 9, 'view_session'),
(37, 'Can add receta', 10, 'add_receta'),
(38, 'Can change receta', 10, 'change_receta'),
(39, 'Can delete receta', 10, 'delete_receta'),
(40, 'Can view receta', 10, 'view_receta');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$IUmCawNM7vf9kwFGdGL6tH$uuBtHwbWYXBveXfjZ5mJ02AOsnHyQdwFDMbNSEjXPno=', '2025-03-26 01:47:50.473496', 1, 'admin', '', '', 'admin@admin.com', 1, 1, '2025-03-25 22:58:22.316129');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(4, 'admin', 'logentry'),
(6, 'auth', 'group'),
(5, 'auth', 'permission'),
(7, 'auth', 'user'),
(8, 'contenttypes', 'contenttype'),
(3, 'gestor', 'cita'),
(2, 'gestor', 'consulta'),
(1, 'gestor', 'paciente'),
(10, 'gestor', 'receta'),
(9, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-03-25 22:42:16.307437'),
(2, 'auth', '0001_initial', '2025-03-25 22:42:17.633052'),
(3, 'admin', '0001_initial', '2025-03-25 22:42:17.980210'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-03-25 22:42:18.064021'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-03-25 22:42:18.183279'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-03-25 22:42:18.574666'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-03-25 22:42:18.766581'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-03-25 22:42:18.914350'),
(9, 'auth', '0004_alter_user_username_opts', '2025-03-25 22:42:18.999384'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-03-25 22:42:19.226889'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-03-25 22:42:19.244432'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-03-25 22:42:19.332590'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-03-25 22:42:19.498151'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-03-25 22:42:19.659128'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-03-25 22:42:19.826745'),
(16, 'auth', '0011_update_proxy_permissions', '2025-03-25 22:42:19.893598'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-03-25 22:42:20.085414'),
(18, 'gestor', '0001_initial', '2025-03-25 22:42:20.472039'),
(19, 'sessions', '0001_initial', '2025-03-25 22:42:20.605662'),
(20, 'gestor', '0002_remove_consulta_altura_remove_consulta_peso_and_more', '2025-03-26 02:16:25.199694'),
(21, 'gestor', '0003_consulta_altura_consulta_peso_and_more', '2025-03-26 02:27:32.739733'),
(22, 'gestor', '0004_receta_fechareceta', '2025-03-26 03:20:49.945137');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('jmevr0qixxsr1syfvea340pgwr9bgtfj', '.eJxVjEEOwiAQRe_C2hAYYUhduvcMZBgGqRqalHbVeHdt0oVu_3vvbyrSutS4dpnjmNVFWXX63RLxU9oO8oPafdI8tWUek94VfdCub1OW1_Vw_w4q9fqtSTINZFiCAUBJCIJYwjlb8ETEaO1gcxApxgAWLobRETiykDw4r94fAtA4Ow:1txFry:naEnI63sog3OEpbqo5DvR_o61DhMj9U7k8yWsvYNxyk', '2025-04-09 01:47:50.532986');

-- --------------------------------------------------------

--
-- Table structure for table `gestor_cita`
--

CREATE TABLE `gestor_cita` (
  `idcita` int(11) NOT NULL,
  `fechacita` date NOT NULL,
  `horacita` varchar(11) NOT NULL,
  `observaciones` varchar(500) NOT NULL,
  `paciente_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gestor_consulta`
--

CREATE TABLE `gestor_consulta` (
  `idconsulta` int(11) NOT NULL,
  `fechaconsulta` date NOT NULL,
  `horaconsulta` time(6) NOT NULL,
  `diagnostico` varchar(500) NOT NULL,
  `paciente_id` int(11) NOT NULL,
  `altura` decimal(10,2) NOT NULL,
  `peso` decimal(10,2) NOT NULL,
  `precioconsulta` decimal(10,2) NOT NULL,
  `presionarterial` varchar(7) NOT NULL,
  `temperatura` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `gestor_consulta`
--

INSERT INTO `gestor_consulta` (`idconsulta`, `fechaconsulta`, `horaconsulta`, `diagnostico`, `paciente_id`, `altura`, `peso`, `precioconsulta`, `presionarterial`, `temperatura`) VALUES
(1, '2025-03-25', '20:28:28.908729', 'wrlfnirg\r\neeoirigoe\r\nerpmeoirvnoenrgoiejrg eoigmoeg', 2, 1.50, 50.00, 25.00, '120/80', 32.00),
(2, '2025-03-25', '21:42:37.040765', 'sdfsdf \r\nsd f\r\ns d\r\nf', 3, 2.00, 43.00, 32.00, '120/89', 33.40);

-- --------------------------------------------------------

--
-- Table structure for table `gestor_paciente`
--

CREATE TABLE `gestor_paciente` (
  `idpaciente` int(11) NOT NULL,
  `nombre` varchar(300) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `telefono` int(10) UNSIGNED NOT NULL CHECK (`telefono` >= 0),
  `sexo` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `gestor_paciente`
--

INSERT INTO `gestor_paciente` (`idpaciente`, `nombre`, `fecha_nacimiento`, `telefono`, `sexo`) VALUES
(1, 'Carlos Hernandez', '1995-11-24', 704532365, 'M'),
(2, 'Julio Cesar Carcamo Flores', '1994-04-30', 84984548, 'M'),
(3, 'Juana Veronica Flores Aguilar', '2001-08-01', 949516984, 'F');

-- --------------------------------------------------------

--
-- Table structure for table `gestor_receta`
--

CREATE TABLE `gestor_receta` (
  `idreceta` int(11) NOT NULL,
  `medicamento` varchar(500) NOT NULL,
  `dosis` varchar(500) NOT NULL,
  `duracion` varchar(500) NOT NULL,
  `indicaciones` varchar(500) NOT NULL,
  `consulta_id` int(11) NOT NULL,
  `fechareceta` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `gestor_receta`
--

INSERT INTO `gestor_receta` (`idreceta`, `medicamento`, `dosis`, `duracion`, `indicaciones`, `consulta_id`, `fechareceta`) VALUES
(1, 'ladsjnbfksdfg\r\ndsfgkjbdsfg\r\ndfsgbk dfg\r\nk', 'lsbnjglknfg\r\ndsfngdfls;kgmndfg\r\nlbg\'s', '30', 'fgdfg;kndfg\r\ndfglndfg\r\ndfgbl', 1, '2025-03-25'),
(2, 'efrsdfs\r\nfds df', 'sdf', '2', 'sdf', 2, '2025-03-25');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `gestor_cita`
--
ALTER TABLE `gestor_cita`
  ADD PRIMARY KEY (`idcita`),
  ADD KEY `gestor_cita_paciente_id_3880604f_fk_gestor_paciente_idpaciente` (`paciente_id`);

--
-- Indexes for table `gestor_consulta`
--
ALTER TABLE `gestor_consulta`
  ADD PRIMARY KEY (`idconsulta`),
  ADD KEY `gestor_consulta_paciente_id_fc9bd660_fk_gestor_pa` (`paciente_id`);

--
-- Indexes for table `gestor_paciente`
--
ALTER TABLE `gestor_paciente`
  ADD PRIMARY KEY (`idpaciente`);

--
-- Indexes for table `gestor_receta`
--
ALTER TABLE `gestor_receta`
  ADD PRIMARY KEY (`idreceta`),
  ADD KEY `gestor_receta_consulta_id_6a41fab7_fk_gestor_consulta_idconsulta` (`consulta_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `gestor_cita`
--
ALTER TABLE `gestor_cita`
  MODIFY `idcita` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gestor_consulta`
--
ALTER TABLE `gestor_consulta`
  MODIFY `idconsulta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `gestor_paciente`
--
ALTER TABLE `gestor_paciente`
  MODIFY `idpaciente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `gestor_receta`
--
ALTER TABLE `gestor_receta`
  MODIFY `idreceta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `gestor_cita`
--
ALTER TABLE `gestor_cita`
  ADD CONSTRAINT `gestor_cita_paciente_id_3880604f_fk_gestor_paciente_idpaciente` FOREIGN KEY (`paciente_id`) REFERENCES `gestor_paciente` (`idpaciente`);

--
-- Constraints for table `gestor_consulta`
--
ALTER TABLE `gestor_consulta`
  ADD CONSTRAINT `gestor_consulta_paciente_id_fc9bd660_fk_gestor_pa` FOREIGN KEY (`paciente_id`) REFERENCES `gestor_paciente` (`idpaciente`);

--
-- Constraints for table `gestor_receta`
--
ALTER TABLE `gestor_receta`
  ADD CONSTRAINT `gestor_receta_consulta_id_6a41fab7_fk_gestor_consulta_idconsulta` FOREIGN KEY (`consulta_id`) REFERENCES `gestor_consulta` (`idconsulta`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
