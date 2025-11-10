-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 04, 2025 at 02:43 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_datawaris`
--

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `idhistory` int(11) NOT NULL,
  `namaFile` varchar(255) NOT NULL,
  `aksi` enum('enkripsi','dekripsi') NOT NULL,
  `waktu` datetime DEFAULT current_timestamp(),
  `email` varchar(255) DEFAULT NULL,
  `users_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`idhistory`, `namaFile`, `aksi`, `waktu`, `email`, `users_id`) VALUES
(15, 'KRSRahasia.enc', 'dekripsi', '2025-06-13 10:54:05', NULL, 1),
(16, 'KRSRahasia.enc', 'dekripsi', '2025-06-13 10:58:03', NULL, 1),
(17, 'KRSRahasia.enc', 'dekripsi', '2025-06-13 11:03:04', NULL, 1),
(18, 'KRSRahasia.pdf', 'enkripsi', '2025-06-13 11:04:23', 'fucyoubit@gmail.com', 1),
(19, 'KRSRahasia.pdf', 'enkripsi', '2025-06-13 11:07:11', 'fucyoubit@gmail.com', 1),
(20, 'KRSRahasia.enc', 'dekripsi', '2025-06-13 11:07:28', NULL, 1),
(21, 'KRSRahasia.enc', 'dekripsi', '2025-06-13 11:10:50', NULL, 1),
(22, 'KRSRahasia.enc', 'dekripsi', '2025-06-13 11:19:13', NULL, 1),
(23, 'KRSRahasia.enc', 'dekripsi', '2025-06-13 11:19:26', NULL, 1),
(24, 'PembayaranRahasia.pdf', 'enkripsi', '2025-06-13 11:38:22', 'fucyoubit@gmail.com', 1),
(25, 'Jadwal Rahasia.pdf', 'enkripsi', '2025-06-15 10:21:06', 'bhnjimko123153@gmail.com', 1),
(26, 'SPAW_Sumarni_05122024.pdf', 'enkripsi', '2025-06-20 09:36:15', 'fucyoubit@gmail.com', 1),
(27, 'SPAW_Sumarni_05122024.enc', 'dekripsi', '2025-06-20 09:37:48', NULL, 1),
(28, 'SPAW_Sumarni_05122024.enc', 'dekripsi', '2025-06-20 09:44:38', NULL, 1),
(29, 'SPAW_Agus Supriyanto_12112024.pdf', 'enkripsi', '2025-06-25 09:52:53', 'fucyoubit@gmail.com', 2),
(30, 'SPAW_Agus_Supriyanto_12112024.enc', 'dekripsi', '2025-06-25 09:53:19', NULL, 2),
(31, 'KRSRahasia.pdf', 'enkripsi', '2025-07-01 14:05:10', 'wow@gmail.com', 1),
(32, 'KRSRahasia.pdf', 'enkripsi', '2025-07-01 14:57:53', 'fucyoubit@gmail.com', 1),
(33, 'KRSRahasia.pdf', 'enkripsi', '2025-07-01 15:02:41', 'fucyoubit@gmail.com', 1),
(34, 'KRSRahasia.pdf', 'enkripsi', '2025-07-01 15:03:20', 'fucyoubit@gmail.com', 1),
(35, 'KRSRahasia.pdf', 'enkripsi', '2025-07-01 15:45:27', 'fucyoubit@gmail.com', 1),
(36, 'KRSRahasia.enc', 'dekripsi', '2025-07-01 15:46:06', NULL, 1),
(37, 'KRSRahasia.enc', 'dekripsi', '2025-07-01 15:51:43', NULL, 1),
(38, 'KRSRahasia.enc', 'dekripsi', '2025-07-01 15:57:23', NULL, 1),
(39, 'SPAW_Sumarni_05122024.pdf', 'enkripsi', '2025-07-02 18:46:40', 'fucyoubit@gmail.com', 1),
(40, 'SPAW_Agus Supriyanto_12112024.pdf', 'enkripsi', '2025-07-02 18:47:53', 'fucyoubit@gmail.com', 1),
(41, 'SPAW_Sukesih_04122024.pdf', 'enkripsi', '2025-07-02 18:48:25', 'fucyoubit@gmail.com', 1),
(42, 'SPAW_Agus Supriyanto_12112024.pdf', 'enkripsi', '2025-07-02 18:49:33', 'fucyoubit@gmail.com', 1),
(43, 'SPAW_Sukesih_04122024.pdf', 'enkripsi', '2025-07-02 18:50:16', 'fucyoubit@gmail.com', 1),
(44, 'SPAW_Santoso_23122024.pdf', 'enkripsi', '2025-07-02 18:50:49', 'fucyoubit@gmail.com', 1),
(45, 'SPAW_Sukenti_05112024.pdf', 'enkripsi', '2025-07-02 18:51:20', 'fucyoubit@gmail.com', 1),
(46, 'SPAW_Gunaryo_23122024.pdf', 'enkripsi', '2025-07-02 18:51:49', 'fucyoubit@gmail.com', 1),
(47, 'SPAW_Basri Allias Baseri_08112024.pdf', 'enkripsi', '2025-07-02 18:52:39', 'fucyoubit@gmail.com', 1),
(48, 'SPAW_Sukenti_05112024.pdf', 'enkripsi', '2025-07-02 20:47:44', 'soegengkarjono.67@gmail.com', 3),
(49, 'SPAW_Sukenti_05112024.enc', 'dekripsi', '2025-07-02 21:01:51', NULL, 3),
(50, 'SPAW_Sukenti_05112024.enc', 'dekripsi', '2025-07-02 21:03:19', NULL, 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `role` enum('superadmin','admin') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `nama_lengkap`, `role`) VALUES
(1, 'ridwan', 'scrypt:32768:8:1$d7y5ZiHuAenWE4zT$6e3cf0f873c1dd53214ea4fd8ebded4b9c069d8c2f1320c5c2778dd82cc64be19becc891f595bbc0209fc5c1d89af3c4c175e65bab2799556382e2239963fee1', 'Mridwan', 'superadmin'),
(2, 'ridwan2', 'scrypt:32768:8:1$WElNoa91gxeOncH5$87d4ee37960fab0f055f50f8a8353a8eee332b0693e8ca11346767e7d016456fd4ea7c9aef863956dc7b7cc540f343258f0f08ee7fd133f807a2a76b67613518', 'MridwanS', 'admin'),
(3, 'SoegengKarjono123', 'scrypt:32768:8:1$TaD3nkcJ9IqqjOaG$a0e001e2ebcd066f68bb68cf822dce270aea6c711dacc82dff02bb820d033e936108d252d9fad12912abc251d6b8c3fa378e79b89c0d6f586190f538d42a94ef', 'Soegeng Karjono', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`idhistory`),
  ADD KEY `fk_history_users_idx` (`users_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username_UNIQUE` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `idhistory` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT `fk_history_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
