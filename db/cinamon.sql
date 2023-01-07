-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 07, 2023 at 07:35 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cinamon`
--

-- --------------------------------------------------------

--
-- Table structure for table `save_movie`
--

CREATE TABLE `save_movie` (
  `id` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `movie_name` varchar(255) NOT NULL,
  `movie_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `save_movie`
--

INSERT INTO `save_movie` (`id`, `id_user`, `movie_name`, `movie_id`) VALUES
(6, 3, 'Avatar: The Way of Water', 76600);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(1, 'opik', 'opik@gmail.com', 'pbkdf2:sha256:260000$EBaN9I16N7l89gK6$b11bdf7f8f2a320f1d7b291c57de93666fe705cbc366cda4739a237f47b3c408'),
(2, 'user', 'user@gmail.com', 'pbkdf2:sha256:260000$bcFfbCwWuMV5rq3H$e9df5fa1ac059b0269bfe8a8b6a12cb99b58ed5e1ebe85588d321c1cc39026c9'),
(3, 'asd', 'asd@gmail.com', 'pbkdf2:sha256:260000$l4THZobiXMIVFjZj$b8081b1833cf7026f6ad0c769e486995747c9465f795ceead91895abc9a2c1c9');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `save_movie`
--
ALTER TABLE `save_movie`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `save_movie`
--
ALTER TABLE `save_movie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `save_movie`
--
ALTER TABLE `save_movie`
  ADD CONSTRAINT `save_movie_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
