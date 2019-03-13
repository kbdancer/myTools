CREATE TABLE IF NOT EXISTS `ipdb` (
  `id` int(11) NOT NULL,
  `range` varchar(50) NOT NULL,
  `location` varchar(200) NOT NULL,
  `type` varchar(100) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `ipdb`
  ADD PRIMARY KEY (`id`);
