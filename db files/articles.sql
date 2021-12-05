-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 02, 2021 at 09:20 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `myflaskapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
CREATE TABLE IF NOT EXISTS `articles` (
  `id` int(200) NOT NULL DEFAULT '1',
  `title` text NOT NULL,
  `author` text NOT NULL,
  `body` text NOT NULL,
  `create_date` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `author`, `body`, `create_date`) VALUES
(1, 'Emergency surgery during the COVID-19 pandemic: what you need to know for practice?', 'suddu', '<p><strong>Abstract</strong></p><p><strong>Section:</strong></p><p>ChooseTop of pageAbstract &lt;&lt;IntroductionMethodsFindingsDiscussionConclusionsReferencesCITING ARTICLES</p><p>&nbsp;</p><p>&nbsp;</p><p><strong>Introduction</strong></p><p>Several articles have been published about the reorganization of surgical activity during the COVID-19 pandemic but few, if any, have focused on the impact that this has had on emergency and trauma surgery. Our aim was to review the most current data on COVID-19 to provide essential suggestions on how to manage the acute abdomen during the pandemic.</p><p>&nbsp;</p><p><strong>Methods</strong></p><p>A systematic review was conducted of the most relevant English language articles on COVID-19 and surgery published between 15 December 2019 and 30 March 2020.</p><p>&nbsp;</p><p><strong>Findings</strong></p><p>Access to the operating theatre is almost exclusively restricted to emergencies and oncological procedures. The use of laparoscopy in COVID-19 positive patients should be cautiously considered. The main risk lies in the presence of the virus in the pneumoperitoneum: the aerosol released in the operating theatre could contaminate both staff and the environment.</p><p>&nbsp;</p><p><strong>Conclusions</strong></p><p>During the COVID-19 pandemic, all efforts should be deployed in order to evaluate the feasibility of postponing surgery until the patient is no longer considered potentially infectious or at risk of perioperative complications. If surgery is deemed necessary, the emergency surgeon must minimise the risk of exposure to the virus by involving a minimal number of healthcare staff and shortening the occupation of the operating theatre. In case of a lack of security measures to enable safe laparoscopy, open surgery should be considered.</p>', '2021-11-28 23:25:24.792539'),
(1, 'Hello This is me', 'suddu', '<p>feidbvfehbvhfd wkvefvjefbkjf envkefvkjfbkbfnv wfbjkebkjebdvjb jrfbrkjergbkjeb</p>', '2021-12-02 21:06:04.841657');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
