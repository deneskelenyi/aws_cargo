-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 06, 2025 at 05:48 PM
-- Server version: 10.11.11-MariaDB-0+deb12u1
-- PHP Version: 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aws`
--

-- --------------------------------------------------------

--
-- Table structure for table `aws_orders`
--

CREATE TABLE `aws_orders` (
  `id` int(11) NOT NULL,
  `tracking` varchar(150) NOT NULL,
  `price` decimal(10,5) NOT NULL,
  `date_system` date NOT NULL,
  `ts_insert` timestamp NOT NULL DEFAULT current_timestamp(),
  `notified` char(1) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ship_tracking`
--

CREATE TABLE `ship_tracking` (
  `id` int(11) NOT NULL,
  `tracking` varchar(150) NOT NULL,
  `description` varchar(500) NOT NULL,
  `ts_insert` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `aws_orders`
--
ALTER TABLE `aws_orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tracking` (`tracking`);

--
-- Indexes for table `ship_tracking`
--
ALTER TABLE `ship_tracking`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tracking` (`tracking`),
  ADD UNIQUE KEY `tracking_2` (`tracking`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `aws_orders`
--
ALTER TABLE `aws_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ship_tracking`
--
ALTER TABLE `ship_tracking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

