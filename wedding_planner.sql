-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 05, 2024 at 08:48 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wedding_planner`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `account_type` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id`, `email`, `password`, `account_type`) VALUES
(1, 'venue@weddingplanner.com', '$2b$12$8Dq2cTW7naLefbODMjct2OTFuwUwGhX/zQLTpZDOQY0TvKHluohRS', 'VENDOR'),
(2, 'catering@weddingplanner.com', '$2b$12$2K48NW4Tw11DvOvX.3l.Ue5X.zhWnZb7BlwHVc6gy8LcKAzt63.tG', 'VENDOR'),
(3, 'florist@weddingplanner.com', '$2b$12$zsQ.nRE6UbXzvJmOVwRLUeuE4tmiTeDQ5ctGyzFOpf6ogMtyJfoAq', 'VENDOR'),
(4, 'photographer@weddingplanner.com', '$2b$12$AXGOL2TEpgZy9FYIpWDNYusiVwm5KcOt7cqAWYz7pqEEeyuDuUQMO', 'VENDOR'),
(5, 'videographer@weddingplanner.com', '$2b$12$1soKJ7LT1GZP2vBcEDyX7uWtvx8mbph9mnvK0m1PuMkKDCbztDx4G', 'VENDOR'),
(6, 'entertainment@weddingplanner.com', '$2b$12$wgdo5om7al07pSRQvQqK/.gOUyaR5D.8BzqrtpCS38WFXBpW5mrs6', 'VENDOR'),
(7, 'user@weddingplanner.com', '$2b$12$yb6n1k6Nqeq7n/2ksQPU8uZaU4i6JXkH33EFqwu6BznsVtBb28r3S', 'USER');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `event_name` varchar(50) NOT NULL,
  `event_date` date NOT NULL,
  `event_time` time NOT NULL,
  `description` text DEFAULT NULL,
  `booking_date` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `profile_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `package_id` int(11) DEFAULT NULL,
  `guests` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

-- --------------------------------------------------------

--
-- Table structure for table `caterer`
--

CREATE TABLE `caterer` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `contact_email` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `city` varchar(120) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`images`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `caterer`
--

INSERT INTO `caterer` (`id`, `name`, `description`, `contact_email`, `address`, `city`, `contact_number`, `images`) VALUES
(1, 'Gourmet Delights Catering', 'Gourmet Delights Catering specializes in crafting exquisite menus tailored to your event\'s theme and dietary preferences. From elegant weddings to corporate luncheons, we ensure every dish is a culinary masterpiece, delighting your guests\' palates and leaving a lasting impression.', 'info@gourmetdelightscatering.com', '12 High Street', 'London', '+44 20 1234 5678', '[\"c58d0ac0-f919-41c8-9c46-805e8c31c7ba.jpg\", \"13e44c0a-aed9-4268-b32b-2f1d898c556c.jpg\"]');

-- --------------------------------------------------------

--
-- Table structure for table `chat_thread`
--

CREATE TABLE `chat_thread` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `vendor_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_thread`
--
-- --------------------------------------------------------

--
-- Table structure for table `entertainment`
--

CREATE TABLE `entertainment` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `contact_email` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `city` varchar(120) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`images`)),
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `entertainment`
--

INSERT INTO `entertainment` (`id`, `name`, `description`, `contact_email`, `address`, `city`, `contact_number`, `images`, `price`) VALUES
(1, 'BeatBox Entertainment', 'BeatBox Entertainment is your premier choice for creating unforgettable experiences on the dance floor. With a diverse range of music genres and state-of-the-art equipment, our talented DJs know how to read the crowd and keep the energy high all night long, ensuring your event is a hit!', 'bookings@beatboxentertainment.co.uk', '90 Groove Road', 'Birmingham', '+44 20 2345 6789', '[\"6b3c49b5-8f15-4369-8b18-76da345178ce.jpg\"]', 300);

-- --------------------------------------------------------

--
-- Table structure for table `florist`
--

CREATE TABLE `florist` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `contact_email` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `city` varchar(120) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`images`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `florist`
--

INSERT INTO `florist` (`id`, `name`, `description`, `contact_email`, `address`, `city`, `contact_number`, `images`) VALUES
(1, 'Petal Perfect Florals', 'Petal Perfect Florals is dedicated to bringing your floral visions to life, whether it\'s a romantic wedding bouquet, stunning centerpieces, or vibrant arrangements for any occasion. With a keen eye for detail and a passion for creativity, we transform spaces into breathtaking floral wonderlands.', 'contact@petalperfectflorals.co.uk', '34 Rose Avenue', 'Manchester', '+44 20 8765 4321', '[\"3d3fb263-ca8c-4dca-898d-a928186d5b4a.jpg\"]');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `message` text NOT NULL,
  `sent_time` datetime DEFAULT NULL,
  `chat_thread_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification`
--

-- --------------------------------------------------------

--
-- Table structure for table `photographer`
--

CREATE TABLE `photographer` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `contact_email` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `city` varchar(120) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`images`)),
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `photographer`
--

INSERT INTO `photographer` (`id`, `name`, `description`, `contact_email`, `address`, `city`, `contact_number`, `images`, `price`) VALUES
(1, 'Eternal Moments Photography', 'Eternal Moments Photography specializes in capturing life\'s most precious moments with an artful eye and a commitment to excellence. From weddings to family portraits, our talented photographers blend creativity and professionalism to deliver stunning images that tell your unique story.', 'hello@eternalmomentsphotography.co.uk', '56 Shutter Lane', 'Edinburgh', '+44 20 3456 7890', '[\"10b56c52-922a-4b3d-93c4-b76a21884bda.png\"]', 1000);

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `venue_id` int(11) DEFAULT NULL,
  `caterer_id` int(11) DEFAULT NULL,
  `entertainment_id` int(11) DEFAULT NULL,
  `videographer_id` int(11) DEFAULT NULL,
  `florist_id` int(11) DEFAULT NULL,
  `photographer_id` int(11) DEFAULT NULL,
  `is_completed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`id`, `account_id`, `service_id`, `venue_id`, `caterer_id`, `entertainment_id`, `videographer_id`, `florist_id`, `photographer_id`, `is_completed`) VALUES
(1, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, 1),
(2, 2, 2, NULL, 1, NULL, NULL, NULL, NULL, 1),
(3, 3, 5, NULL, NULL, NULL, NULL, 1, NULL, 1),
(4, 6, 6, NULL, NULL, 1, NULL, NULL, NULL, 1),
(5, 4, 3, NULL, NULL, NULL, NULL, NULL, 1, 1),
(6, 5, 4, NULL, NULL, NULL, 1, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `refund_policy`
--

CREATE TABLE `refund_policy` (
  `id` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  `description` text NOT NULL,
  `profile_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `refund_policy`
--

INSERT INTO `refund_policy` (`id`, `days`, `description`, `profile_id`) VALUES
(1, 3, 'Refund is only available for bookings that have more time than 6 Day.. Once paid for less than 6 Days are not refunded', 1);

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `service` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `service`) VALUES
(1, 'venue'),
(2, 'catering'),
(3, 'photographer'),
(4, 'videographer'),
(5, 'florist'),
(6, 'entertainment');

-- --------------------------------------------------------

--
-- Table structure for table `todo`
--

CREATE TABLE `todo` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `account_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vendor_menu`
--

CREATE TABLE `vendor_menu` (
  `id` int(11) NOT NULL,
  `caterer_id` int(11) DEFAULT NULL,
  `florist_id` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vendor_menu`
--

INSERT INTO `vendor_menu` (`id`, `caterer_id`, `florist_id`, `name`, `description`, `price`) VALUES
(1, 1, NULL, '2 Course Meal per person', 'Includes Desi Item and Sweet Dish of your choice', 20),
(2, NULL, 1, 'Rose Decore', 'Full roses at your venue and cover the space up to 70 Square Foot with 50kg Flowers', 400),
(3, 1, NULL, '5 Course meal', 'We include everything from side dishes to fancy oens', 900);

-- --------------------------------------------------------

--
-- Table structure for table `venue`
--

CREATE TABLE `venue` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `price` float NOT NULL,
  `number_of_guests` int(11) NOT NULL,
  `contact_email` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `city` varchar(120) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`images`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `venue`
--

INSERT INTO `venue` (`id`, `name`, `description`, `price`, `number_of_guests`, `contact_email`, `address`, `city`, `contact_number`, `images`) VALUES
(1, 'Royal Albert Hall', 'The Royal Albert Hall is a concert hall on the northern edge of South Kensington, London, England. It has a seating capacity of 5,272. Since the hall\'s opening by Queen Victoria in 1871, the world\'s leading artists from many performance genres have appeared on its', 400, 1500, 'royal@weddingplanner.com', '23 ABC Street', 'London', '+44 123 456 789', '[\"bc3a0a44-f9a4-40af-94f0-7e1a74bb461d.jpg\", \"98db5c63-d8c9-4b48-aa8e-03a43537fe5f.jpg\"]');

-- --------------------------------------------------------

--
-- Table structure for table `videographer`
--

CREATE TABLE `videographer` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `contact_email` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `city` varchar(120) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`images`)),
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `videographer`
--

INSERT INTO `videographer` (`id`, `name`, `description`, `contact_email`, `address`, `city`, `contact_number`, `images`, `price`) VALUES
(1, 'Cinematic Dreams Productions', 'Cinematic Dreams Productions is dedicated to creating timeless wedding films that capture the essence of your special day in a cinematic and emotive style. With a passion for storytelling and attention to detail, we turn fleeting moments into cherished memories that you\'ll treasure for a lifetime.', 'inquiries@cinematicdreams.co.uk', '78 Lens Street', 'Bristol', '+44 20 7890 1234', '[\"5bced96e-e1db-42af-b991-d8622262d3a2.jpg\"]', 1500);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `profile_id` (`profile_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `caterer`
--
ALTER TABLE `caterer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chat_thread`
--
ALTER TABLE `chat_thread`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `vendor_id` (`vendor_id`);

--
-- Indexes for table `entertainment`
--
ALTER TABLE `entertainment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `florist`
--
ALTER TABLE `florist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chat_thread_id` (`chat_thread_id`),
  ADD KEY `sender_id` (`sender_id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `photographer`
--
ALTER TABLE `photographer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_id` (`account_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `venue_id` (`venue_id`),
  ADD KEY `caterer_id` (`caterer_id`),
  ADD KEY `entertainment_id` (`entertainment_id`),
  ADD KEY `videographer_id` (`videographer_id`),
  ADD KEY `florist_id` (`florist_id`),
  ADD KEY `photographer_id` (`photographer_id`);

--
-- Indexes for table `refund_policy`
--
ALTER TABLE `refund_policy`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `profile_id` (`profile_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `todo`
--
ALTER TABLE `todo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_id` (`account_id`);

--
-- Indexes for table `vendor_menu`
--
ALTER TABLE `vendor_menu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `caterer_id` (`caterer_id`),
  ADD KEY `florist_id` (`florist_id`);

--
-- Indexes for table `venue`
--
ALTER TABLE `venue`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `videographer`
--
ALTER TABLE `videographer`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `caterer`
--
ALTER TABLE `caterer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `chat_thread`
--
ALTER TABLE `chat_thread`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `entertainment`
--
ALTER TABLE `entertainment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `florist`
--
ALTER TABLE `florist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `photographer`
--
ALTER TABLE `photographer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `profile`
--
ALTER TABLE `profile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `refund_policy`
--
ALTER TABLE `refund_policy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `todo`
--
ALTER TABLE `todo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vendor_menu`
--
ALTER TABLE `vendor_menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `venue`
--
ALTER TABLE `venue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `videographer`
--
ALTER TABLE `videographer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`profile_id`) REFERENCES `profile` (`id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`),
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`package_id`) REFERENCES `vendor_menu` (`id`);

--
-- Constraints for table `chat_thread`
--
ALTER TABLE `chat_thread`
  ADD CONSTRAINT `chat_thread_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `account` (`id`),
  ADD CONSTRAINT `chat_thread_ibfk_2` FOREIGN KEY (`vendor_id`) REFERENCES `account` (`id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`chat_thread_id`) REFERENCES `chat_thread` (`id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `account` (`id`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`);

--
-- Constraints for table `profile`
--
ALTER TABLE `profile`
  ADD CONSTRAINT `profile_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  ADD CONSTRAINT `profile_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`),
  ADD CONSTRAINT `profile_ibfk_3` FOREIGN KEY (`venue_id`) REFERENCES `venue` (`id`),
  ADD CONSTRAINT `profile_ibfk_4` FOREIGN KEY (`caterer_id`) REFERENCES `caterer` (`id`),
  ADD CONSTRAINT `profile_ibfk_5` FOREIGN KEY (`entertainment_id`) REFERENCES `entertainment` (`id`),
  ADD CONSTRAINT `profile_ibfk_6` FOREIGN KEY (`videographer_id`) REFERENCES `videographer` (`id`),
  ADD CONSTRAINT `profile_ibfk_7` FOREIGN KEY (`florist_id`) REFERENCES `florist` (`id`),
  ADD CONSTRAINT `profile_ibfk_8` FOREIGN KEY (`photographer_id`) REFERENCES `photographer` (`id`);

--
-- Constraints for table `refund_policy`
--
ALTER TABLE `refund_policy`
  ADD CONSTRAINT `refund_policy_ibfk_1` FOREIGN KEY (`profile_id`) REFERENCES `profile` (`id`);

--
-- Constraints for table `todo`
--
ALTER TABLE `todo`
  ADD CONSTRAINT `todo_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`);

--
-- Constraints for table `vendor_menu`
--
ALTER TABLE `vendor_menu`
  ADD CONSTRAINT `vendor_menu_ibfk_1` FOREIGN KEY (`caterer_id`) REFERENCES `caterer` (`id`),
  ADD CONSTRAINT `vendor_menu_ibfk_2` FOREIGN KEY (`florist_id`) REFERENCES `florist` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
