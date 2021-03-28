CREATE DATABASE `spider` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

use spider;

CREATE TABLE `实习僧` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `salary_tip` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `company_tip` varchar(255) DEFAULT NULL,
  `job_benefits` varchar(255) DEFAULT NULL,
  `company_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1082 DEFAULT CHARSET=utf8mb4;