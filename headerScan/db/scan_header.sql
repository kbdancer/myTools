-- phpMyAdmin SQL Dump
-- version 4.4.15.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2017-05-23 10:39:39
-- 服务器版本： 5.5.48-log
-- PHP Version: 5.4.45

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `scan_header`
--

-- --------------------------------------------------------

--
-- 表的结构 `info`
--

CREATE TABLE IF NOT EXISTS `info` (
  `id` int(11) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `country` varchar(50) NOT NULL DEFAULT '未识别',
  `province` varchar(50) NOT NULL DEFAULT '未识别',
  `city` varchar(50) DEFAULT '未识别',
  `isp` varchar(50) DEFAULT '未识别',
  `port` varchar(5) NOT NULL,
  `server` varchar(50) NOT NULL,
  `title` varchar(120) NOT NULL,
  `client` varchar(20) NOT NULL,
  `hash` varchar(32) NOT NULL,
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `ports`
--

CREATE TABLE IF NOT EXISTS `ports` (
  `id` int(11) NOT NULL,
  `port` int(11) NOT NULL,
  `enable` int(11) NOT NULL DEFAULT '1',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `info`
--
ALTER TABLE `info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `id_2` (`id`),
  ADD KEY `id_3` (`id`),
  ADD KEY `hash` (`hash`),
  ADD KEY `id_4` (`id`),
  ADD KEY `area` (`country`),
  ADD KEY `id_5` (`id`),
  ADD KEY `id_6` (`id`),
  ADD KEY `ip` (`ip`),
  ADD KEY `hash_2` (`hash`),
  ADD KEY `id_7` (`id`),
  ADD KEY `hash_3` (`hash`),
  ADD KEY `id_8` (`id`),
  ADD KEY `id_9` (`id`),
  ADD KEY `hash_4` (`hash`),
  ADD KEY `id_10` (`id`),
  ADD KEY `hash_5` (`hash`),
  ADD KEY `id_11` (`id`),
  ADD KEY `hash_6` (`hash`);

--
-- Indexes for table `ports`
--
ALTER TABLE `ports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `info`
--
ALTER TABLE `info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ports`
--
ALTER TABLE `ports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
