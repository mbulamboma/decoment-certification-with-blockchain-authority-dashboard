-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 08 sep. 2023 à 16:13
-- Version du serveur : 10.4.22-MariaDB
-- Version de PHP : 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `certification_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(250) NOT NULL,
  `email` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `admins`
--

INSERT INTO `admins` (`id`, `username`, `email`, `password`) VALUES
(1, 'mbula mboma', 'mbula.gilberto@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f');

-- --------------------------------------------------------

--
-- Structure de la table `departements`
--

CREATE TABLE `departements` (
  `id` int(11) NOT NULL,
  `label` varchar(250) NOT NULL,
  `fac_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `departements`
--

INSERT INTO `departements` (`id`, `label`, `fac_id`, `created_at`) VALUES
(1, 'Science de base', 1, '2023-08-24 16:46:37'),
(2, 'Génie électrique et Informatique', 1, '2023-08-24 16:46:37'),
(3, 'Génie Civil', 1, '2023-08-24 16:46:37'),
(4, 'Génie Mécanique', 1, '2023-08-24 16:46:37');

-- --------------------------------------------------------

--
-- Structure de la table `documents`
--

CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `label` varchar(250) NOT NULL,
  `price` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `documents`
--

INSERT INTO `documents` (`id`, `label`, `price`, `created_at`) VALUES
(1, 'RELEVE DE COTES', 10, '2023-08-24 16:18:29'),
(2, 'LETTRE DE STAGE', 5, '2023-08-24 16:19:07');

-- --------------------------------------------------------

--
-- Structure de la table `facultes`
--

CREATE TABLE `facultes` (
  `id` int(11) NOT NULL,
  `label` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `facultes`
--

INSERT INTO `facultes` (`id`, `label`, `created_at`) VALUES
(1, 'Polytechnique', '2023-08-24 16:40:37');

-- --------------------------------------------------------

--
-- Structure de la table `orientations`
--

CREATE TABLE `orientations` (
  `id` int(11) NOT NULL,
  `label` varchar(250) NOT NULL,
  `dep_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `orientations`
--

INSERT INTO `orientations` (`id`, `label`, `dep_id`, `created_at`) VALUES
(1, 'Science de base', 1, '2023-08-24 17:09:29'),
(2, 'Informatique', 2, '2023-08-24 17:09:29'),
(3, 'Electronique', 2, '2023-08-24 17:09:29'),
(4, 'Electro-énergétique', 2, '2023-08-24 17:09:29'),
(5, 'Hydraulique et construction Hydraulique', 3, '2023-08-24 17:09:29'),
(6, 'structure et ouvrage d\'art', 3, '2023-08-24 17:09:29'),
(7, 'Electromécanique', 4, '2023-08-24 17:09:29'),
(8, 'construction mécanique', 0, '2023-08-24 17:09:29');

-- --------------------------------------------------------

--
-- Structure de la table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `req_id` int(11) NOT NULL,
  `email` varchar(250) NOT NULL,
  `phone` varchar(150) NOT NULL,
  `paid` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `payments`
--

INSERT INTO `payments` (`id`, `req_id`, `email`, `phone`, `paid`, `created_at`) VALUES
(1, 1, 'william.mutombo@odyssey-tec.com', '0814243950', 1, '2023-08-25 00:04:38');

-- --------------------------------------------------------

--
-- Structure de la table `requests`
--

CREATE TABLE `requests` (
  `id` int(11) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `student_id` varchar(150) NOT NULL,
  `document_id` varchar(100) NOT NULL,
  `ipfs_hash` varchar(250) NOT NULL,
  `faculty` varchar(150) NOT NULL,
  `department` varchar(150) NOT NULL,
  `orientation` varchar(150) NOT NULL,
  `promotion` varchar(100) NOT NULL,
  `academic_year` varchar(50) NOT NULL,
  `requested_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `doc_hash` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `requests`
--

INSERT INTO `requests` (`id`, `full_name`, `student_id`, `document_id`, `ipfs_hash`, `faculty`, `department`, `orientation`, `promotion`, `academic_year`, `requested_at`, `doc_hash`) VALUES
(1, 'Mbula Mboma', '1235484', 'RELEVE DE COTES', 'http://127.0.0.1:8080/ipfs/QmPctTWjWaetUXiTKaMAC1hC8MWMFaM29fmjxYiwRoUNc6', 'Polytechnique', 'Science de base', 'Science de base', 'L2', '2022-2023', '2023-08-24 17:18:50', '');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `departements`
--
ALTER TABLE `departements`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `facultes`
--
ALTER TABLE `facultes`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `orientations`
--
ALTER TABLE `orientations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `departements`
--
ALTER TABLE `departements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `facultes`
--
ALTER TABLE `facultes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT pour la table `orientations`
--
ALTER TABLE `orientations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
