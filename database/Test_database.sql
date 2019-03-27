CREATE DATABASE  IF NOT EXISTS `obedy_test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `obedy_test`;
-- MySQL dump 10.13  Distrib 8.0.14, for Win64 (x86_64)
--
-- Host: localhost    Database: obedy_test
-- ------------------------------------------------------
-- Server version	8.0.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `obedy`
--

DROP TABLE IF EXISTS `obedy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `obedy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `datum` date NOT NULL,
  `osobni_cislo` varchar(16) CHARACTER SET utf8 COLLATE utf8_czech_ci NOT NULL,
  `karta` text CHARACTER SET utf8 COLLATE utf8_czech_ci NOT NULL,
  `jmeno` text CHARACTER SET utf8 COLLATE utf8_czech_ci NOT NULL,
  `trida` text CHARACTER SET utf8 COLLATE utf8_czech_ci NOT NULL,
  `cislo_obedu` tinyint(4) NOT NULL DEFAULT '0',
  `stav` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0-nic,1-objednano,2-vydano',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obedy`
--

LOCK TABLES `obedy` WRITE;
/*!40000 ALTER TABLE `obedy` DISABLE KEYS */;
INSERT INTO `obedy` VALUES (1,'2016-09-05','33113','127FB2B6','Josef Novák','4L',2,2),(2,'2016-09-05','33138','E47F410E','Martin Stárek','4B',1,2),(3,'2016-09-05','03210','ACFA5B47','Lukáš Zapletal','3A',1,1),(4,'2016-09-05','33113','A455420E','Kryštof Stejskal','4B',2,1);
/*!40000 ALTER TABLE `obedy` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-27  9:59:28
