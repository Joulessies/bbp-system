-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 01, 2026 at 02:15 AM
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
-- Database: `bbp_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `assigned_to` int(11) DEFAULT NULL,
  `business_name` varchar(255) NOT NULL,
  `business_type` varchar(100) NOT NULL,
  `business_address` text NOT NULL,
  `business_description` text NOT NULL,
  `capital_investment` decimal(15,2) NOT NULL,
  `employees` int(11) NOT NULL,
  `owner_first_name` varchar(50) NOT NULL,
  `owner_last_name` varchar(50) NOT NULL,
  `owner_address` text NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `valid_id_number` varchar(100) NOT NULL,
  `tin_number` varchar(100) DEFAULT NULL,
  `status` enum('Pending','Under Review','Approved','Ready for Pickup','Returned for Correction','Rejected') DEFAULT 'Pending',
  `priority` enum('Low','Medium','High') DEFAULT 'Low',
  `completeness_score` int(11) DEFAULT 0,
  `remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `application_type` enum('New','Renewal') DEFAULT 'New',
  `previous_permit_no` varchar(100) DEFAULT NULL,
  `ownership_type` varchar(50) DEFAULT NULL,
  `dti_sec_cda_reg_no` varchar(100) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `date_of_establishment` date DEFAULT NULL,
  `owner_gender` enum('Male','Female','Other') DEFAULT NULL,
  `owner_nationality` varchar(50) DEFAULT NULL,
  `is_same_address` tinyint(1) DEFAULT 0,
  `employees_male` int(11) DEFAULT 0,
  `employees_female` int(11) DEFAULT 0,
  `employees_resident` int(11) DEFAULT 0,
  `delivery_vehicles` int(11) DEFAULT 0,
  `rental_status` enum('Owned','Rented') DEFAULT NULL,
  `lessor_name` varchar(100) DEFAULT NULL,
  `lessor_address` text DEFAULT NULL,
  `lessor_contact` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`id`, `user_id`, `assigned_to`, `business_name`, `business_type`, `business_address`, `business_description`, `capital_investment`, `employees`, `owner_first_name`, `owner_last_name`, `owner_address`, `contact_number`, `email`, `valid_id_number`, `tin_number`, `status`, `priority`, `completeness_score`, `remarks`, `created_at`, `updated_at`, `application_type`, `previous_permit_no`, `ownership_type`, `dti_sec_cda_reg_no`, `registration_date`, `date_of_establishment`, `owner_gender`, `owner_nationality`, `is_same_address`, `employees_male`, `employees_female`, `employees_resident`, `delivery_vehicles`, `rental_status`, `lessor_name`, `lessor_address`, `lessor_contact`) VALUES
(1, 3, 18, 'Juan\'s Sari-Sari Store', 'Retail', '123 Main St, Caloocan', 'Neighborhood convenience store', 50000.00, 2, 'Juan', 'Dela Cruz', '123 Main St', '09171234567', 'juan@example.com', 'ID-12345', NULL, 'Returned for Correction', 'Medium', 85, 'Updated by staffokokok', '2026-04-19 23:52:47', '2026-04-22 02:17:50', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(2, 3, 2, 'Caloocan Coffee Shop', 'Food Service', '456 Plaza Ave, Caloocan', 'Specialty coffee and pastries', 250000.00, 5, 'Juan', 'Dela Cruz', '123 Main St', '09171234567', 'juan@example.com', 'ID-12345', NULL, 'Pending', 'High', 95, NULL, '2026-04-19 23:52:47', '2026-04-19 23:52:47', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(3, 7, 2, 'Mira\'s Beauty Parlor', 'Personal Service', '789 Beauty Way, Caloocan', 'Full service hair and nail salon', 120000.00, 3, 'Mira', 'Applicant', '789 Beauty Way', '09189998877', 'mira@example.com', 'ID-99887', NULL, 'Pending', 'Medium', 70, NULL, '2026-04-19 23:52:47', '2026-04-20 02:41:26', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(4, 7, 15, 'Quick Fix Electronics', '', '101 Tech Blvd, Caloocan', 'Gadget and appliance repair', 75000.00, 1, 'Mira', 'Applicant', '789 Beauty Way', '09189998877', 'mira@example.com', 'ID-99887', '', 'Under Review', 'Low', 100, 'Updated by staff', '2026-04-19 23:52:47', '2026-04-22 02:10:45', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(5, 8, 6, 'Quick Fix Electronics', 'Automotive', '101 Tech Blvd, Caloocan', 'Gadget and appliance repair', 75000.00, 1, 'Mira', 'Applicant', '789 Beauty Way', '09189998877', 'mira@example.com', 'ID-99887', '', 'Under Review', 'High', 0, 'Updated by staff', '2026-04-19 23:59:26', '2026-04-20 03:30:51', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(6, 8, 2, 'Vape Shop', 'Retail', 'Test Address Caloocan', 'Test Business', 500000.00, 2, 'Mira Juliana', 'Alcantara', 'Test Address', '09565400304', 'mirajulianaa1006@gmail.com', '123456789', '', 'Pending', 'Medium', 50, 'Updated by staff', '2026-04-20 00:04:37', '2026-04-20 03:30:51', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(7, 8, 2, 'Donut', 'Food Service', 'Test Address Caloocan', 'Test', 10000.00, 1, 'Mira', 'Alcantara', 'lot 34, Amparo subd', '09565400304', 'mirajulianaa1006@gmail.com', 'Test', '', 'Pending', 'Low', 100, 'Updated by staff', '2026-04-20 00:13:57', '2026-04-20 03:30:51', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(8, 8, 15, 'Burger', 'Food Service', 'Test Address Caloocan', 'TEST', 10000.00, 5, 'Mira', 'Alcantara', 'lot 34, Amparo subd', '09565400304', 'mirajulianaa1006@gmail.com', '236465', '', 'Under Review', 'High', 50, 'Updated by staff', '2026-04-20 00:38:51', '2026-04-30 18:06:06', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(9, 8, 19, 'Kapehan Ni Juan', 'Food Service', 'Test Address Caloocan', 'test', 1000.00, 1, 'Juliana', 'Alcantara', 'lot 34, Amparo subd', '09565613', 'mirajulianaa1006@gmail.com', '236465', '', 'Approved', 'Low', 0, 'Updated by staff', '2026-04-20 00:41:58', '2026-04-30 23:07:42', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(10, 8, 19, 'Sari Sari', 'Food Service', 'Test Address Caloocan', 'TEST', 10000.00, 0, 'Mira', 'Alcantara', 'lot 34, Amparo subd', '09565400304', 'mirajulianaa1006@gmail.com', '236465', '', 'Approved', 'Low', 50, 'Updated by staff', '2026-04-20 02:26:54', '2026-04-30 13:29:29', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(11, 3, 19, 'Python ML Test Gas Station', 'Others', '123 ML Street', 'Testing Python ML Integration', 1500000.00, 5, 'Juan', 'Dela Cruz', '123 ML Street, Barangay 183, Caloocan City', '09123456789', 'juan@example.com', '123456789', '', 'Rejected', 'Low', 0, 'Updated by staff', '2026-04-20 12:00:23', '2026-04-29 17:31:08', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(12, 8, 15, 'Test Business', 'Automotive', '101 Tech Blvd, Caloocan', 'Gadget and appliance repair', 2000000.00, 1, 'Mira', 'Applicant', '789 Beauty Way', '09189998877', 'mira@example.com', 'ID-99887', '', 'Pending', 'Low', 0, 'Updated by staff', '2026-04-20 12:20:36', '2026-04-20 12:27:33', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(13, 17, 19, 'Fixed ML Gas Station', 'Automotive', '123 Caloocan St, Barangay 183', 'Gas station with automotive services', 2000000.00, 5, 'Test', 'User', 'Test Address', '09123456789', 'test_user@example.com', '123456789', '', 'Under Review', 'High', 100, 'Updated by staff', '2026-04-20 12:37:51', '2026-04-29 17:29:06', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(14, 8, 19, 'Food Test', 'Food Service', 'lot 34, Amparo subd', 'Test', 500000.00, 0, 'Mira', 'Alcantara', 'lot 34, Amparo subd', '09565613', 'mirajulianaa1006@gmail.com', '236465', '', 'Ready for Pickup', 'Medium', 80, 'Updated by staff', '2026-04-20 12:53:52', '2026-04-30 19:24:52', 'New', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL),
(15, 8, NULL, 'Sari Sari', 'Food Service', 'Test Address Caloocan', 'TEST', 10000.00, 0, 'Mira', 'Alcantara', '0', '09565400304', '0', '', '', 'Approved', 'Low', 40, 'Updated by staff', '2026-04-30 17:20:13', '2026-04-30 18:47:14', 'Renewal', '10', 'Single Proprietorship', '', NULL, NULL, '', '', 0, 0, 0, 0, 0, '', '', '', ''),
(16, 1, NULL, 'Test', '', '123', '', 0.00, 0, 'A', 'B', '0', '', '0', '', '', 'Pending', 'Low', 0, NULL, '2026-04-30 17:25:03', '2026-04-30 17:25:03', 'Renewal', '1', '', '', NULL, NULL, '', '', 0, 0, 0, 0, 0, '', '', '', ''),
(17, 8, NULL, 'Sari Sari', 'Food Service', 'lot 34, Amparo subd', '', 321321.00, 5, 'Mira', 'Alcantara', '0', '09565400304', '0', '', '565656', 'Ready for Pickup', 'Medium', 40, 'Updated by staff', '2026-04-30 18:04:21', '2026-04-30 20:14:32', 'New', NULL, 'Single Proprietorship', '43242', '2026-05-13', '2026-05-28', 'Female', 'filipino', 1, 1, 4, 3, 0, 'Owned', '', '', ''),
(18, 8, NULL, 'Food Test', 'Food Service', 'lot 34, Amparo subd', '', 500000.00, 7, 'Mira', 'Alcantara', '0', '09565613', '0', '', '565656', 'Ready for Pickup', 'Medium', 50, 'Updated by staff', '2026-04-30 18:11:23', '2026-04-30 18:35:13', 'Renewal', '14', 'Single Proprietorship', '43242', '2026-04-30', '2026-05-15', 'Female', 'filipino', 1, 4, 3, 3, 0, '', '', '', ''),
(19, 8, NULL, 'SM Fairview', 'Food Service', 'lot 34, Amparo subd', '', 24324324.00, 12, 'Mira', 'Alcantara', '0', '09565400304', '0', '', '565656', 'Pending', 'High', 50, NULL, '2026-04-30 18:19:25', '2026-04-30 18:19:25', 'New', NULL, 'Single Proprietorship', '43242', '2026-05-21', '2026-05-21', 'Female', 'filipino', 1, 6, 6, 5, 0, '', '', '', ''),
(20, 8, NULL, 'Kapehan Ni Juan', 'Food Service', 'Test Address Caloocan', 'test', 1000.00, 7, 'Juliana', 'Alcantara', '0', '09565613', '0', '', '565656', 'Under Review', 'Low', 50, 'Updated by staff', '2026-04-30 18:45:52', '2026-04-30 19:56:35', 'Renewal', '9', 'Single Proprietorship', '43242', '2026-05-13', '2026-05-12', 'Female', 'filipino', 1, 4, 3, 3, 0, '', '', '', ''),
(21, 8, 19, 'Sari Sari', 'Food Service', 'lot 34, Amparo subd', '', 321321.00, 5, 'Mira', 'Alcantara', '0', '09565400304', '0', '', '565656', 'Pending', 'Medium', 15, NULL, '2026-04-30 20:05:58', '2026-04-30 22:06:54', 'Renewal', '17', 'Single Proprietorship', '43242', '2026-05-13', '2026-05-28', 'Female', 'filipino', 1, 1, 4, 3, 0, 'Owned', '', '', ''),
(22, 8, 19, 'Cafe ', 'Food Service', 'lot 34, Amparo subd', '', 24325.00, 4, 'Mira', 'Alcantara', '0', '09565400304', '0', '', '565656', 'Under Review', 'Low', 15, 'Updated by staff', '2026-04-30 22:14:04', '2026-04-30 22:58:59', 'New', NULL, 'Single Proprietorship', '43242', '2026-05-13', '2026-05-29', 'Female', 'filipino', 1, 2, 2, 2, 0, '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `audit_logs`
--

CREATE TABLE `audit_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `audit_logs`
--

INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `ip_address`, `created_at`) VALUES
(1, 1, 'System initialization after XAMPP recovery', '127.0.0.1', '2026-04-19 23:52:47'),
(2, 1, 'Restored database from master backup', '127.0.0.1', '2026-04-19 23:52:47'),
(3, 1, 'Added Mira Applicant to the system', '127.0.0.1', '2026-04-19 23:52:47'),
(4, 1, 'Updated staff user account ID: 4 (Tricia Alcantara)', '127.0.0.1', '2026-04-19 23:52:47'),
(5, 3, 'Logged in as Juan Dela Cruz', '127.0.0.1', '2026-04-19 23:52:47'),
(7, 1, 'User logged in', '::1', '2026-04-19 23:53:14'),
(8, 7, 'User logged in', '::1', '2026-04-19 23:53:46'),
(9, 2, 'Updated application ID 4 status to Under Review', '::1', '2026-04-19 23:54:34'),
(10, 2, 'Updated application ID 4 status to Returned for Correction', '::1', '2026-04-19 23:54:45'),
(11, 8, 'User registered', '::1', '2026-04-19 23:58:50'),
(12, 8, 'User logged in', '::1', '2026-04-19 23:59:03'),
(13, 8, 'Submitted application ID: 5', '::1', '2026-04-19 23:59:26'),
(14, 8, 'Submitted application ID: 6', '::1', '2026-04-20 00:04:37'),
(15, 2, 'Updated application ID 6 status to Under Review', '::1', '2026-04-20 00:05:58'),
(16, 2, 'Updated application ID 6 status to Returned for Correction', '::1', '2026-04-20 00:07:03'),
(17, 8, 'Updated application ID 6 (resubmitted after correction)', '::1', '2026-04-20 00:07:44'),
(18, 1, 'Assigned application ID 6 to staff user 2', '::1', '2026-04-20 00:08:11'),
(19, 2, 'Updated application ID 6 status to Under Review', '::1', '2026-04-20 00:09:22'),
(20, 2, 'Updated application ID 6 status to Approved', '::1', '2026-04-20 00:09:33'),
(21, 2, 'Updated application ID 6 status to Ready for Pickup', '::1', '2026-04-20 00:09:51'),
(22, 2, 'Updated application ID 6 status to Under Review', '::1', '2026-04-20 00:10:22'),
(23, 2, 'Updated application ID 6 status to Rejected', '::1', '2026-04-20 00:10:34'),
(24, 2, 'Updated application ID 6 status to Under Review', '::1', '2026-04-20 00:11:17'),
(25, 2, 'Updated application ID 6 status to Returned for Correction', '::1', '2026-04-20 00:11:52'),
(26, 8, 'Updated application ID 6 (resubmitted after correction)', '::1', '2026-04-20 00:12:44'),
(27, 8, 'Submitted application ID: 7', '::1', '2026-04-20 00:13:57'),
(28, 1, 'Assigned application ID 7 to staff user 2', '::1', '2026-04-20 00:18:49'),
(29, 2, 'Updated application ID 7 status to Returned for Correction', '::1', '2026-04-20 00:19:30'),
(30, 8, 'Updated application ID 7 (resubmitted after correction)', '::1', '2026-04-20 00:19:45'),
(31, 2, 'Updated application ID 4 status to Under Review', '::1', '2026-04-20 00:21:17'),
(32, 2, 'Updated application ID 7 status to Under Review', '::1', '2026-04-20 00:32:00'),
(33, 2, 'User logged in', '::1', '2026-04-20 00:33:44'),
(34, 2, 'Updated application ID 7 status to Ready for Pickup', '::1', '2026-04-20 00:34:10'),
(35, 2, 'Updated application ID 7 status to Under Review', '::1', '2026-04-20 00:34:21'),
(36, 1, 'Assigned application ID 5 to staff user 5', '::1', '2026-04-20 00:34:45'),
(37, 1, 'Assigned application ID 5 to staff user 6', '::1', '2026-04-20 00:34:46'),
(38, 2, 'Updated application ID 7 status to Approved', '::1', '2026-04-20 00:35:30'),
(39, 2, 'Updated application ID 7 status to Under Review', '::1', '2026-04-20 00:35:56'),
(40, 2, 'Updated application ID 7 status to Rejected', '::1', '2026-04-20 00:36:06'),
(41, 2, 'Updated application ID 7 status to Under Review', '::1', '2026-04-20 00:36:53'),
(42, 2, 'Updated application ID 7 status to Returned for Correction', '::1', '2026-04-20 00:37:42'),
(43, 8, 'Submitted application ID: 8', '::1', '2026-04-20 00:38:51'),
(44, 2, 'Updated application ID 8 status to Under Review', '::1', '2026-04-20 00:39:02'),
(45, 2, 'Updated application ID 8 status to Returned for Correction', '::1', '2026-04-20 00:39:29'),
(46, 8, 'Updated application ID 8 (resubmitted after correction)', '::1', '2026-04-20 00:39:51'),
(47, 8, 'Submitted application ID: 9', '::1', '2026-04-20 00:41:58'),
(48, 2, 'Updated application ID 9 status to Under Review', '::1', '2026-04-20 00:42:16'),
(49, 2, 'Updated application ID 9 status to Approved', '::1', '2026-04-20 00:42:33'),
(50, 8, 'User logged in', '::1', '2026-04-20 00:46:05'),
(51, 8, 'Updated application ID 7 (resubmitted after correction)', '::1', '2026-04-20 00:53:11'),
(52, 2, 'Updated application ID 7 status to Returned for Correction', '::1', '2026-04-20 00:53:32'),
(53, 8, 'Updated application ID 7 (resubmitted after correction)', '::1', '2026-04-20 00:54:10'),
(54, 2, 'Updated application ID 7 status to Returned for Correction', '::1', '2026-04-20 00:54:18'),
(55, 8, 'Updated application ID 7 (resubmitted after correction)', '::1', '2026-04-20 00:58:05'),
(56, 2, 'Updated application ID 7 status to Returned for Correction', '::1', '2026-04-20 00:58:35'),
(57, 8, 'Updated application ID 7 (resubmitted after correction)', '::1', '2026-04-20 01:00:59'),
(58, 2, 'Updated application ID 8 status to Under Review', '::1', '2026-04-20 01:13:44'),
(59, 1, 'Created staff account: stafftest@caloocan.gov.ph', '::1', '2026-04-20 01:15:19'),
(60, 1, 'Changed user ID 2 status to Inactive', '::1', '2026-04-20 01:15:36'),
(61, 1, 'Changed user ID 2 status to Active', '::1', '2026-04-20 01:15:56'),
(62, 2, 'Updated application ID 8 status to Approved', '::1', '2026-04-20 01:17:18'),
(63, 6, 'User logged in', '::1', '2026-04-20 01:22:41'),
(64, 6, 'Updated application ID 5 status to Under Review', '::1', '2026-04-20 01:22:49'),
(65, 6, 'Updated application ID 4 status to Under Review', '::1', '2026-04-20 01:23:11'),
(66, 6, 'Updated application ID 5 status to Approved', '::1', '2026-04-20 01:24:32'),
(67, 6, 'Updated application ID 5 status to Under Review', '::1', '2026-04-20 01:24:47'),
(68, 6, 'Updated application ID 5 status to Rejected', '::1', '2026-04-20 01:25:00'),
(69, 6, 'Updated application ID 5 status to Under Review', '::1', '2026-04-20 01:25:17'),
(70, 6, 'Updated application ID 5 status to Returned for Correction', '::1', '2026-04-20 01:25:31'),
(71, 8, 'Updated application ID 5 (resubmitted after correction)', '::1', '2026-04-20 01:26:34'),
(72, 6, 'Updated application ID 5 status to Under Review', '::1', '2026-04-20 01:26:50'),
(73, 6, 'Updated application ID 5 status to Approved', '::1', '2026-04-20 01:27:03'),
(74, 6, 'Updated application ID 5 status to Ready for Pickup', '::1', '2026-04-20 01:27:10'),
(75, 1, 'Updated staff user account ID: 9', '::1', '2026-04-20 01:27:59'),
(76, 1, 'Changed user ID 2 status to Inactive', '::1', '2026-04-20 01:30:53'),
(77, 1, 'Changed user ID 2 status to Active', '::1', '2026-04-20 01:31:05'),
(78, 1, 'Changed user ID 2 status to Inactive', '::1', '2026-04-20 01:31:16'),
(79, 1, 'Changed user ID 2 status to Active', '::1', '2026-04-20 01:31:27'),
(80, 1, 'Changed user ID 2 status to Inactive', '::1', '2026-04-20 01:48:11'),
(81, 1, 'Changed user ID 2 status to Active', '::1', '2026-04-20 01:48:15'),
(82, 1, 'Updated staff user account ID: 6', '::1', '2026-04-20 01:48:52'),
(83, 1, 'Reset password for user account ID: 6', '::1', '2026-04-20 01:49:09'),
(84, 1, 'Permanently deleted user account ID: 4', '::1', '2026-04-20 01:52:41'),
(85, 1, 'Updated staff user account ID: 5', '::1', '2026-04-20 01:54:18'),
(86, 1, 'Created staff account: staffmira@caloocan.gov.ph', '::1', '2026-04-20 02:02:53'),
(87, 1, 'Updated staff user account ID: 10', '::1', '2026-04-20 02:03:28'),
(88, 1, 'Created staff account: staffsample@caloocan.gov.ph', '::1', '2026-04-20 02:04:42'),
(89, 1, 'Permanently deleted user account ID: 11', '::1', '2026-04-20 02:05:11'),
(90, 1, 'Created staff account: test@caloocan.gov.ph', '::1', '2026-04-20 02:08:44'),
(91, 1, 'Permanently deleted user account ID: 12', '::1', '2026-04-20 02:09:03'),
(92, 1, 'Created staff account: test@caloocan.gov.ph', '::1', '2026-04-20 02:14:00'),
(93, 1, 'Updated staff user account ID: 13', '::1', '2026-04-20 02:17:45'),
(94, 1, 'Created staff account: staff6@caloocan.gov.ph', '::1', '2026-04-20 02:24:56'),
(95, 1, 'Updated staff user account ID: 14', '::1', '2026-04-20 02:25:11'),
(96, 8, 'Submitted application ID: 10', '::1', '2026-04-20 02:26:54'),
(97, 6, 'Updated application ID 10 status to Under Review', '::1', '2026-04-20 02:27:22'),
(98, 6, 'Updated application ID 5 status to Under Review', '::1', '2026-04-20 02:27:37'),
(99, 6, 'Updated application ID 10 status to Approved', '::1', '2026-04-20 02:27:49'),
(100, 6, 'Updated application ID 5 status to Ready for Pickup', '::1', '2026-04-20 02:32:07'),
(101, 6, 'Updated application ID 5 status to Under Review', '::1', '2026-04-20 02:35:00'),
(102, 6, 'Updated application ID 5 status to Returned for Correction', '::1', '2026-04-20 02:35:08'),
(103, 8, 'Updated application ID 5 (resubmitted after correction)', '::1', '2026-04-20 02:36:38'),
(104, 6, 'Updated application ID 5 status to Rejected', '::1', '2026-04-20 02:40:57'),
(105, 1, 'Assigned application ID 4 to staff user 2', '::1', '2026-04-20 02:41:17'),
(106, 1, 'Assigned application ID 3 to staff user 2', '::1', '2026-04-20 02:41:26'),
(107, 1, 'Created staff account: test2@caloocan.gov.ph', '::1', '2026-04-20 02:42:04'),
(108, 6, 'Updated application ID 5 status to Ready for Pickup', '::1', '2026-04-20 02:53:01'),
(109, 6, 'Updated application ID 5 status to Under Review', '::1', '2026-04-20 02:53:53'),
(110, 6, 'Updated application ID 1 status to Returned for Correction', '::1', '2026-04-20 02:54:00'),
(111, 6, 'Updated application ID 8 status to Ready for Pickup', '::1', '2026-04-20 02:54:20'),
(112, 1, 'User logged in', '::1', '2026-04-20 06:05:55'),
(113, 1, 'User logged in', '::1', '2026-04-20 06:06:19'),
(114, 8, 'User logged in', '::1', '2026-04-20 10:38:06'),
(115, 2, 'User logged in', '::1', '2026-04-20 10:38:46'),
(116, 1, 'User logged in', '::1', '2026-04-20 10:39:12'),
(117, 1, 'Created staff account: test3@caloocan.gov.ph', '::1', '2026-04-20 10:40:43'),
(118, 1, 'Updated staff user account ID: 16', '::1', '2026-04-20 10:41:09'),
(119, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:46:13'),
(120, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:46:27'),
(121, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:46:46'),
(122, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:47:03'),
(123, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:49:06'),
(124, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:51:14'),
(125, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:51:42'),
(126, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:56:10'),
(127, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 10:59:35'),
(128, 1, 'Updated staff user account ID: 2', '::1', '2026-04-20 11:04:17'),
(129, 15, 'User logged in', '::1', '2026-04-20 11:17:02'),
(130, 1, 'Updated staff user account ID: 15', '::1', '2026-04-20 11:17:14'),
(131, 1, 'Reset password for user account ID: 15', '::1', '2026-04-20 11:17:40'),
(132, 3, 'User logged in', '::1', '2026-04-20 11:58:00'),
(133, 3, 'Submitted application ID: 11', '::1', '2026-04-20 12:00:23'),
(134, 3, 'User logged in', '::1', '2026-04-20 12:03:18'),
(135, 15, 'User logged in', '::1', '2026-04-20 12:18:58'),
(136, 8, 'Submitted application ID: 12', '::1', '2026-04-20 12:20:36'),
(137, 1, 'Assigned application ID 12 to staff user 15', '::1', '2026-04-20 12:25:24'),
(138, 15, 'Updated application ID 12 status to Under Review', '::1', '2026-04-20 12:25:35'),
(139, 15, 'Updated application ID 12 status to Returned for Correction', '::1', '2026-04-20 12:25:41'),
(140, 8, 'Updated application ID 12 (resubmitted after correction)', '::1', '2026-04-20 12:27:33'),
(141, 17, 'User registered', '::1', '2026-04-20 12:35:41'),
(142, 17, 'User logged in', '::1', '2026-04-20 12:36:01'),
(143, 17, 'Submitted application ID: 13', '::1', '2026-04-20 12:37:51'),
(144, 8, 'Submitted application ID: 14', '::1', '2026-04-20 12:53:52'),
(145, 8, 'User logged in', '::1', '2026-04-20 13:24:46'),
(146, 1, 'User logged in', '::1', '2026-04-20 13:25:40'),
(147, 1, 'Reset password for user account ID: 15', '::1', '2026-04-20 13:26:16'),
(148, 15, 'User logged in', '::1', '2026-04-20 13:26:40'),
(149, 1, 'Assigned application ID 8 to staff user 15', '::1', '2026-04-20 13:27:27'),
(150, 8, 'Password reset via email', '::1', '2026-04-20 16:12:03'),
(151, 8, 'User logged in', '::1', '2026-04-20 16:12:11'),
(152, 8, 'Password reset via email', '::1', '2026-04-20 16:23:01'),
(153, 8, 'User logged in', '::1', '2026-04-20 16:23:12'),
(154, 1, 'Created staff account: test4@caloocan.gov.ph', '::1', '2026-04-20 17:46:07'),
(155, 18, 'User logged in', '::1', '2026-04-20 17:46:35'),
(156, 18, 'Set permanent password on first login', '::1', '2026-04-20 17:49:38'),
(157, 18, 'User logged in', '::1', '2026-04-20 17:50:21'),
(158, 1, 'Reset password for user account ID: 18', '::1', '2026-04-20 17:51:00'),
(159, 18, 'User logged in', '::1', '2026-04-20 17:51:45'),
(160, 1, 'Created staff account: test5@caloocan.gov.ph', '::1', '2026-04-20 18:07:09'),
(161, 19, 'User logged in', '::1', '2026-04-20 18:07:36'),
(162, 19, 'Set permanent password on first login', '::1', '2026-04-20 18:08:11'),
(163, 1, 'Reset password for user account ID: 19', '::1', '2026-04-20 18:08:26'),
(164, 19, 'User logged in', '::1', '2026-04-20 18:10:16'),
(165, 19, 'Set permanent password on first login', '::1', '2026-04-20 18:10:39'),
(166, 1, 'Changed user ID 19 status to Inactive', '::1', '2026-04-20 18:28:56'),
(167, 1, 'Changed user ID 19 status to Active', '::1', '2026-04-20 18:29:04'),
(168, 1, 'Reset password for user account ID: 19', '::1', '2026-04-20 18:29:16'),
(169, 19, 'User logged in', '::1', '2026-04-20 18:29:37'),
(170, 19, 'Set permanent password on first login', '::1', '2026-04-20 18:29:52'),
(171, 8, 'User logged in', '::1', '2026-04-21 18:12:47'),
(172, 19, 'User logged in', '::1', '2026-04-21 18:16:35'),
(173, 1, 'User logged in', '::1', '2026-04-21 18:17:05'),
(174, 19, 'User logged in', '::1', '2026-04-21 18:17:37'),
(175, 1, 'Assigned application ID 13 to staff user 18', '::1', '2026-04-21 18:17:55'),
(176, 1, 'Updated staff user account ID: 19', '::1', '2026-04-21 18:18:32'),
(177, 1, 'Updated staff user account ID: 18', '::1', '2026-04-21 18:18:44'),
(178, 1, 'Assigned application ID 13 to staff user 19', '::1', '2026-04-21 18:18:54'),
(179, 19, 'Updated application ID 13 status to Rejected', '::1', '2026-04-21 18:19:15'),
(180, 1, 'User logged in', '::1', '2026-04-21 23:07:05'),
(181, 19, 'User logged in', '::1', '2026-04-21 23:07:21'),
(182, 20, 'User registered', '::1', '2026-04-21 23:10:20'),
(183, 20, 'User logged in', '::1', '2026-04-21 23:10:58'),
(184, 8, 'User logged in', '::1', '2026-04-21 23:14:37'),
(185, 8, 'User logged in', '::1', '2026-04-21 23:21:47'),
(186, 19, 'Updated application ID 14 status to Under Review', '::1', '2026-04-21 23:22:21'),
(187, 1, 'Reset password for user account ID: 15', '::1', '2026-04-21 23:32:58'),
(188, 15, 'User logged in', '::1', '2026-04-21 23:33:06'),
(189, 15, 'Set permanent password on first login', '::1', '2026-04-21 23:33:15'),
(190, 8, 'User logged in', '::1', '2026-04-21 23:36:38'),
(191, 15, 'Updated application ID 14 status to Under Review', '::1', '2026-04-21 23:48:23'),
(192, 15, 'Updated application ID 1 status to Returned for Correction', '::1', '2026-04-22 01:21:51'),
(193, 15, 'Updated application ID 11 status to Rejected', '::1', '2026-04-22 01:22:19'),
(194, 1, 'User logged in', '::1', '2026-04-22 01:54:28'),
(195, 8, 'User logged in', '::1', '2026-04-22 02:02:20'),
(196, 1, 'Assigned application ID 4 to staff user 15', '::1', '2026-04-22 02:10:45'),
(197, 1, 'Assigned application ID 1 to staff user 18', '::1', '2026-04-22 02:17:50'),
(198, 8, 'User logged in', '::1', '2026-04-22 04:10:33'),
(199, 15, 'Updated application ID 14 status to Under Review', '::1', '2026-04-22 04:22:49'),
(200, 15, 'Updated application ID 14 status to Rejected', '::1', '2026-04-22 04:23:35'),
(201, 8, 'User logged in', '::1', '2026-04-24 20:52:17'),
(202, 1, 'User logged in', '::1', '2026-04-24 20:52:40'),
(203, 19, 'User logged in', '::1', '2026-04-24 20:52:51'),
(204, 8, 'User logged in', '::1', '2026-04-29 16:55:57'),
(205, 1, 'User logged in', '::1', '2026-04-29 16:57:05'),
(206, 19, 'User logged in', '::1', '2026-04-29 17:01:07'),
(207, 19, 'Updated application ID 13 status to Under Review', '::1', '2026-04-29 17:29:06'),
(208, 1, 'Assigned application ID 14 to staff user 19', '::1', '2026-04-29 17:31:05'),
(209, 1, 'Assigned application ID 11 to staff user 19', '::1', '2026-04-29 17:31:08'),
(210, 19, 'Updated application ID 14 status to Under Review', '::1', '2026-04-29 17:31:20'),
(211, 8, 'User logged in', '::1', '2026-04-30 10:53:49'),
(212, 19, 'User logged in', '::1', '2026-04-30 10:54:02'),
(213, 1, 'User logged in', '::1', '2026-04-30 10:54:15'),
(214, 1, 'Updated application ID 9 status to Ready for Pickup', '::1', '2026-04-30 13:29:17'),
(215, 1, 'Assigned application ID 10 to staff user 19', '::1', '2026-04-30 13:29:29'),
(217, 8, 'User logged in', '::1', '2026-04-30 17:18:53'),
(218, 8, 'Submitted application ID: 15', '::1', '2026-04-30 17:20:13'),
(219, 1, 'Submitted application ID: 16', '::1', '2026-04-30 17:25:03'),
(220, 8, 'Submitted application ID: 17', '::1', '2026-04-30 18:04:21'),
(221, 1, 'Updated application ID 8 status to Under Review', '::1', '2026-04-30 18:06:06'),
(222, 19, 'Updated application ID 14 status to Approved', '::1', '2026-04-30 18:08:53'),
(223, 8, 'Submitted application ID: 18', '::1', '2026-04-30 18:11:23'),
(224, 8, 'Submitted application ID: 19', '::1', '2026-04-30 18:19:25'),
(225, 19, 'Updated application ID 9 status to Approved', '::1', '2026-04-30 18:20:24'),
(226, 19, 'Updated application ID 18 status to Approved', '::1', '2026-04-30 18:34:55'),
(227, 1, 'Updated application ID 18 status to Ready for Pickup', '::1', '2026-04-30 18:35:13'),
(228, 8, 'Renewal Application Submitted for Kapehan Ni Juan (ID: 20)', '::1', '2026-04-30 18:45:52'),
(229, 19, 'Updated application ID 15 status to Approved', '::1', '2026-04-30 18:47:14'),
(230, 19, 'Updated application ID 17 status to Approved', '::1', '2026-04-30 18:47:29'),
(231, 1, 'Updated application ID 14 status to Ready for Pickup', '::1', '2026-04-30 19:24:52'),
(232, 19, 'Updated application ID 20 status to Under Review', '::1', '2026-04-30 19:34:33'),
(233, 19, 'Updated application ID 20 status to Approved', '::1', '2026-04-30 19:35:04'),
(234, 19, 'Updated application ID 20 status to Under Review', '::1', '2026-04-30 19:56:35'),
(235, 8, 'Renewal Application Submitted for Sari Sari (ID: 21)', '::1', '2026-04-30 20:05:58'),
(236, 19, 'Updated application ID 17 status to Ready for Pickup', '::1', '2026-04-30 20:14:32'),
(237, 19, 'User logged in', '::1', '2026-04-30 21:52:16'),
(238, 8, 'User logged in', '::1', '2026-04-30 21:52:46'),
(239, 1, 'User logged in', '::1', '2026-04-30 21:52:54'),
(240, 8, 'User logged in', '::1', '2026-04-30 22:04:59'),
(241, 1, 'Assigned application ID 21 to staff user 19', '::1', '2026-04-30 22:06:54'),
(242, 19, 'User logged in', '::1', '2026-04-30 22:07:15'),
(243, 8, 'New Application Submitted for Cafe  (ID: 22)', '::1', '2026-04-30 22:14:04'),
(244, 19, 'Updated application ID 22 status to Under Review', '::1', '2026-04-30 22:44:05'),
(245, 1, 'Assigned application ID 22 to staff user 19', '::1', '2026-04-30 22:58:59'),
(246, 1, 'Assigned application ID 9 to staff user 19', '::1', '2026-04-30 23:07:42'),
(247, 1, 'Created staff account: staff7@caloocan.gov.ph', '::1', '2026-04-30 23:08:32'),
(248, 1, 'Updated staff user account ID: 22', '::1', '2026-04-30 23:08:51'),
(249, 1, 'Changed user ID 22 status to Inactive', '::1', '2026-04-30 23:09:09'),
(250, 1, 'Changed user ID 22 status to Active', '::1', '2026-04-30 23:09:15'),
(251, 1, 'Reset password for user account ID: 22', '::1', '2026-04-30 23:09:42'),
(252, 1, 'Reset password for user account ID: 22', '::1', '2026-04-30 23:09:48'),
(253, 22, 'User logged in', '::1', '2026-04-30 23:10:25'),
(254, 22, 'Set permanent password on first login', '::1', '2026-04-30 23:10:39'),
(255, 19, 'User logged in', '::1', '2026-04-30 23:10:59'),
(256, 23, 'User registered', '::1', '2026-05-01 00:03:17'),
(257, 24, 'User registered', '::1', '2026-05-01 00:10:53'),
(258, 24, 'User verified email address', '::1', '2026-05-01 00:11:23'),
(259, 24, 'User logged in', '::1', '2026-05-01 00:11:34');

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `document_type` varchar(100) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`id`, `application_id`, `document_type`, `file_path`, `uploaded_at`) VALUES
(1, 1, 'Valid Government ID', 'backend/uploads/sample_id.pdf', '2026-04-19 23:52:47'),
(2, 1, 'Barangay Clearance', 'backend/uploads/sample_clearance.pdf', '2026-04-19 23:52:47'),
(3, 2, 'Business Plan', 'backend/uploads/coffee_plan.pdf', '2026-04-19 23:52:47'),
(4, 3, 'DTI Registration', 'backend/uploads/mira_dti.pdf', '2026-04-19 23:52:47'),
(5, 5, 'Valid Government ID', 'backend/uploads/1776643166_HCIN312_PROJECT-PROPOSAL-PAPER_BSIT3-6.pdf', '2026-04-19 23:59:26'),
(6, 5, 'Barangay Clearance', 'backend/uploads/1776643166_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-19 23:59:26'),
(7, 6, 'Valid Government ID', 'backend/uploads/1776643477_HCIN312_PROJECT-PROPOSAL-PAPER_BSIT3-6.pdf', '2026-04-20 00:04:37'),
(8, 6, 'Barangay Clearance', 'backend/uploads/1776643477_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-20 00:04:37'),
(9, 6, 'Business Plan', 'backend/uploads/1776643477_ALCANTARA_NETACADCheckpointScores_BSIT3-6.pdf', '2026-04-20 00:04:37'),
(10, 6, 'validIdDoc', 'uploads/1776643964_validIdDoc_HCIN312_PROJECT-PROPOSAL-PAPER_BSIT3-6.pdf', '2026-04-20 00:07:44'),
(11, 6, 'barangayClearance', 'uploads/1776643964_barangayClearance_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-20 00:07:44'),
(12, 6, 'businessPlan', 'uploads/1776643964_businessPlan_ALCANTARA_NETACADCheckpointScores_BSIT3-6.pdf', '2026-04-20 00:07:44'),
(13, 6, 'dtiRegistration', 'uploads/1776643964_dtiRegistration_logo.jpg', '2026-04-20 00:07:44'),
(14, 6, 'sanitaryPermit', 'uploads/1776643964_sanitaryPermit_IT-and-DS-Preventive-Maintenance-and-Inventory-Tracker.pdf', '2026-04-20 00:07:44'),
(15, 6, 'firePermit', 'uploads/1776643964_firePermit_ALCANTARA_LABTESTPRELIMS_IT3-6_02262026.pdf', '2026-04-20 00:07:44'),
(16, 6, 'otherDocuments', 'uploads/1776643964_otherDocuments_Request Letter IT.pdf', '2026-04-20 00:07:44'),
(17, 7, 'Valid Government ID', 'backend/uploads/1776644037_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-20 00:13:57'),
(18, 7, 'Barangay Clearance', 'backend/uploads/1776644037_IT-and-DS-Preventive-Maintenance-and-Inventory-Tracker.pdf', '2026-04-20 00:13:57'),
(19, 7, 'Business Plan', 'backend/uploads/1776644037_ALCANTARA_LABTESTPRELIMS_IT3-6_02262026.pdf', '2026-04-20 00:13:57'),
(20, 7, 'DTI Registration', 'backend/uploads/1776644037_Request Letter IT.pdf', '2026-04-20 00:13:57'),
(21, 7, 'Sanitary Permit', 'backend/uploads/1776644037_Request Letter IT.pdf', '2026-04-20 00:13:57'),
(22, 7, 'Fire Safety Certificate', 'backend/uploads/1776644037_Request Letter IT.pdf', '2026-04-20 00:13:57'),
(23, 7, 'Other Documents', 'backend/uploads/1776644037_Admin.jpg', '2026-04-20 00:13:57'),
(24, 7, 'validIdDoc', 'backend/uploads/1776646859_validIdDoc_ALCANTARA_NETACADCheckpointScores_BSIT3-6.pdf', '2026-04-20 00:19:45'),
(25, 8, 'Valid Government ID', 'backend/uploads/1776645531_logo.jpg', '2026-04-20 00:38:51'),
(26, 8, 'Barangay Clearance', 'backend/uploads/1776645531_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-20 00:38:51'),
(27, 8, 'Business Plan', 'backend/uploads/1776645531_HCIN312_PROJECT-PROPOSAL-PAPER_BSIT3-6.pdf', '2026-04-20 00:38:51'),
(28, 8, 'validIdDoc', 'backend/uploads/1776645591_validIdDoc_logo.jpg', '2026-04-20 00:39:51'),
(29, 9, 'Valid Government ID', 'backend/uploads/1776645718_logo.jpg', '2026-04-20 00:41:58'),
(30, 7, 'barangayClearance', 'backend/uploads/1776646859_barangayClearance_logo.jpg', '2026-04-20 00:53:11'),
(31, 7, 'businessPlan', 'backend/uploads/1776646859_businessPlan_ALCANTARA_NETACADCheckpointScores_BSIT3-6.pdf', '2026-04-20 00:53:11'),
(32, 5, 'validIdDoc', 'backend/uploads/1776652598_validIdDoc_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-20 01:26:34'),
(33, 5, 'barangayClearance', 'backend/uploads/1776652598_barangayClearance_ALCANTARA_NETACADCheckpointScores_BSIT3-6.pdf', '2026-04-20 01:26:34'),
(34, 5, 'businessPlan', 'backend/uploads/1776652598_businessPlan_ALCANTARA_NETACADCheckpointScores_BSIT3-6.pdf', '2026-04-20 01:26:34'),
(35, 10, 'Valid Government ID', 'backend/uploads/1776652014_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-20 02:26:54'),
(36, 10, 'Barangay Clearance', 'backend/uploads/1776652014_logo.jpg', '2026-04-20 02:26:54'),
(37, 10, 'Business Plan', 'backend/uploads/1776652014_ALCANTARA_NETACADCheckpointScores_BSIT3-6.pdf', '2026-04-20 02:26:54'),
(38, 11, 'Valid Government ID', 'backend/uploads/1776686423_dummy.txt', '2026-04-20 12:00:23'),
(39, 11, 'Barangay Clearance', 'backend/uploads/1776686423_dummy.txt', '2026-04-20 12:00:23'),
(40, 11, 'Business Plan', 'backend/uploads/1776686423_dummy.txt', '2026-04-20 12:00:23'),
(41, 11, 'DTI Registration', 'backend/uploads/1776686423_dummy.txt', '2026-04-20 12:00:23'),
(42, 11, 'Sanitary Permit', 'backend/uploads/1776686423_dummy.txt', '2026-04-20 12:00:23'),
(43, 11, 'Fire Safety Certificate', 'backend/uploads/1776686423_dummy.txt', '2026-04-20 12:00:23'),
(44, 11, 'Other Documents', 'backend/uploads/1776686423_dummy.txt', '2026-04-20 12:00:23'),
(45, 12, 'Valid Government ID', 'backend/uploads/1776687636_BBP_Official_Report_2026-04-20.pdf', '2026-04-20 12:20:36'),
(46, 12, 'Barangay Clearance', 'backend/uploads/1776687636_REPORT.pdf', '2026-04-20 12:20:36'),
(47, 12, 'Business Plan', 'backend/uploads/1776687636_ALCANTARA_MIDTERMLABORATORYTEST_BSIT3-6_04162026.pdf', '2026-04-20 12:20:36'),
(48, 12, 'validIdDoc', 'backend/uploads/1776688053_validIdDoc_validID.jpg', '2026-04-20 12:27:33'),
(49, 12, 'barangayClearance', 'backend/uploads/1776688053_barangayClearance_barangayClearance.jpg', '2026-04-20 12:27:33'),
(50, 12, 'businessPlan', 'backend/uploads/1776688053_businessPlan_businessPlanProposal.png', '2026-04-20 12:27:33'),
(51, 13, 'Valid Government ID', 'backend/uploads/1776688671_dummy.txt', '2026-04-20 12:37:51'),
(52, 13, 'Barangay Clearance', 'backend/uploads/1776688671_dummy.txt', '2026-04-20 12:37:51'),
(53, 13, 'Business Plan', 'backend/uploads/1776688671_dummy.txt', '2026-04-20 12:37:51'),
(54, 13, 'DTI Registration', 'backend/uploads/1776688671_dummy.txt', '2026-04-20 12:37:51'),
(55, 13, 'Sanitary Permit', 'backend/uploads/1776688671_dummy.txt', '2026-04-20 12:37:51'),
(56, 13, 'Fire Safety Certificate', 'backend/uploads/1776688671_dummy.txt', '2026-04-20 12:37:51'),
(57, 13, 'Other Documents', 'backend/uploads/1776688671_dummy.txt', '2026-04-20 12:37:51'),
(58, 14, 'Valid Government ID', 'backend/uploads/1776689632_barangayClearance.jpg', '2026-04-20 12:53:52'),
(59, 14, 'Barangay Clearance', 'backend/uploads/1776689632_businessPlanProposal.png', '2026-04-20 12:53:52'),
(60, 14, 'Business Plan', 'backend/uploads/1776689632_validID.jpg', '2026-04-20 12:53:52'),
(61, 14, 'DTI Registration', 'backend/uploads/1776689632_BBP_Official_Report_2026-04-20.pdf', '2026-04-20 12:53:52'),
(62, 14, 'Sanitary Permit', 'backend/uploads/1776689632_REPORT.pdf', '2026-04-20 12:53:52'),
(63, 15, 'DTI / SEC / CDA Registration', 'backend/uploads/1777569613_template.jpg', '2026-04-30 17:20:13'),
(64, 15, 'Fire Safety Inspection Certificate', 'backend/uploads/1777569613_template.jpg', '2026-04-30 17:20:13'),
(65, 15, 'Affidavit of Undertaking', 'backend/uploads/1777569613_businesspermit.pdf', '2026-04-30 17:20:13'),
(66, 15, 'Business Permit Application Form (Signed)', 'backend/uploads/1777569613_ALCANTARA_NETACADNetworkDefense_BSIT3-6_04132026.pdf', '2026-04-30 17:20:13'),
(67, 15, 'Locational Clearance', 'backend/uploads/1777569613_CUSTOMER_INTERFACE.png', '2026-04-30 17:20:13'),
(68, 17, 'DTI / SEC / CDA Registration', 'backend/uploads/1777572261_template.jpg', '2026-04-30 18:04:21'),
(69, 17, 'Fire Safety Inspection Certificate', 'backend/uploads/1777572261_ADMIN_INTERFACE.png', '2026-04-30 18:04:21'),
(70, 17, 'Affidavit of Undertaking', 'backend/uploads/1777572261_ADMIN_INTERFACE.png', '2026-04-30 18:04:21'),
(71, 17, 'Business Permit Application Form (Signed)', 'backend/uploads/1777572261_ADMIN_INTERFACE.png', '2026-04-30 18:04:21'),
(72, 17, 'Locational Clearance', 'backend/uploads/1777572261_CUSTOMER_INTERFACE.png', '2026-04-30 18:04:21'),
(73, 18, 'DTI / SEC / CDA Registration', 'backend/uploads/1777572683_template.jpg', '2026-04-30 18:11:23'),
(74, 18, 'Fire Safety Inspection Certificate', 'backend/uploads/1777572683_template.jpg', '2026-04-30 18:11:23'),
(75, 18, 'Affidavit of Undertaking', 'backend/uploads/1777572683_template.jpg', '2026-04-30 18:11:23'),
(76, 18, 'Business Permit Application Form (Signed)', 'backend/uploads/1777572683_template.jpg', '2026-04-30 18:11:23'),
(77, 18, 'Locational Clearance', 'backend/uploads/1777572683_template.jpg', '2026-04-30 18:11:23'),
(78, 18, 'Sketch / Location Plan', 'backend/uploads/1777572683_template.jpg', '2026-04-30 18:11:23'),
(79, 19, 'DTI / SEC / CDA Registration', 'backend/uploads/1777573165_template.jpg', '2026-04-30 18:19:25'),
(80, 19, 'Fire Safety Inspection Certificate', 'backend/uploads/1777573165_template.jpg', '2026-04-30 18:19:25'),
(81, 19, 'Affidavit of Undertaking', 'backend/uploads/1777573165_template.jpg', '2026-04-30 18:19:25'),
(82, 19, 'Business Permit Application Form (Signed)', 'backend/uploads/1777573165_template.jpg', '2026-04-30 18:19:25'),
(83, 19, 'Locational Clearance', 'backend/uploads/1777573165_template.jpg', '2026-04-30 18:19:25'),
(84, 19, 'Sketch / Location Plan', 'backend/uploads/1777573165_template.jpg', '2026-04-30 18:19:25'),
(85, 20, 'DTI / SEC / CDA Registration', 'backend/uploads/1777574752_template.jpg', '2026-04-30 18:45:52'),
(86, 20, 'Fire Safety Inspection Certificate', 'backend/uploads/1777574752_template.jpg', '2026-04-30 18:45:52'),
(87, 20, 'Affidavit of Undertaking', 'backend/uploads/1777574752_template.jpg', '2026-04-30 18:45:52'),
(88, 20, 'Business Permit Application Form (Signed)', 'backend/uploads/1777574752_template.jpg', '2026-04-30 18:45:52'),
(89, 20, 'Locational Clearance', 'backend/uploads/1777574752_template.jpg', '2026-04-30 18:45:52'),
(90, 20, 'Sketch / Location Plan', 'backend/uploads/1777574752_template.jpg', '2026-04-30 18:45:52'),
(91, 21, 'DTI / SEC / CDA Registration', 'backend/uploads/1777579558_template.jpg', '2026-04-30 20:05:58'),
(92, 22, 'DTI / SEC / CDA Registration', 'backend/uploads/1777587244_template.jpg', '2026-04-30 22:14:04');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `type` enum('info','success','warning','error') DEFAULT 'info',
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `title`, `message`, `type`, `is_read`, `created_at`) VALUES
(3, 3, 'Status Update', 'Your application for Juan\'s Sari-Sari Store is now Under Review.', 'info', 0, '2026-04-19 23:52:47'),
(4, 7, 'Application Approved', 'Congratulations! Your application for Quick Fix Electronics has been approved.', 'success', 0, '2026-04-19 23:52:47'),
(6, 7, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: All documents verified', 'info', 0, '2026-04-19 23:54:34'),
(8, 7, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-19 23:54:45'),
(14, 5, 'New Application', 'New application submitted: Quick Fix Electronics (ID: 5)', 'info', 0, '2026-04-19 23:59:26'),
(15, 6, 'New Application', 'New application submitted: Quick Fix Electronics (ID: 5)', 'info', 0, '2026-04-19 23:59:26'),
(22, 5, 'New Application', 'New application submitted: Vape Shop (ID: 6)', 'info', 0, '2026-04-20 00:04:37'),
(23, 6, 'New Application', 'New application submitted: Vape Shop (ID: 6)', 'info', 0, '2026-04-20 00:04:37'),
(41, 8, 'Status Update', 'Your application for \"Vape Shop\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:11:17'),
(43, 8, 'Status Update', 'Your application for \"Vape Shop\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:11:52'),
(46, 8, 'Application Submitted', 'Your application for Donut has been submitted and is currently Pending.', 'info', 0, '2026-04-20 00:13:57'),
(50, 5, 'New Application', 'New application submitted: Donut (ID: 7)', 'info', 0, '2026-04-20 00:13:57'),
(51, 6, 'New Application', 'New application submitted: Donut (ID: 7)', 'info', 0, '2026-04-20 00:13:57'),
(54, 2, 'New Assignment', 'A new application (ID: 7) has been assigned to you for review.', 'info', 0, '2026-04-20 00:18:49'),
(55, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:19:30'),
(57, 2, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Donut (ID: 7).', 'info', 0, '2026-04-20 00:19:45'),
(58, 7, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:21:17'),
(60, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:32:00'),
(62, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:34:10'),
(64, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:34:21'),
(66, 5, 'New Assignment', 'A new application (ID: 5) has been assigned to you for review.', 'info', 0, '2026-04-20 00:34:45'),
(67, 6, 'New Assignment', 'A new application (ID: 5) has been assigned to you for review.', 'info', 0, '2026-04-20 00:34:46'),
(68, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Approved. Staff Remarks: TEST', 'info', 0, '2026-04-20 00:35:30'),
(70, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Under Review. Staff Remarks: TEST', 'info', 0, '2026-04-20 00:35:56'),
(72, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Rejected. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:36:06'),
(74, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:36:53'),
(76, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:37:42'),
(78, 8, 'Application Submitted', 'Your application for Burger has been submitted and is currently Pending.', 'info', 0, '2026-04-20 00:38:51'),
(80, 2, 'New Application', 'New application submitted: Burger (ID: 8)', 'info', 0, '2026-04-20 00:38:51'),
(82, 5, 'New Application', 'New application submitted: Burger (ID: 8)', 'info', 0, '2026-04-20 00:38:51'),
(83, 6, 'New Application', 'New application submitted: Burger (ID: 8)', 'info', 0, '2026-04-20 00:38:51'),
(86, 8, 'Status Update', 'Your application for \"Burger\" has been updated to: Under Review.', 'info', 0, '2026-04-20 00:39:02'),
(88, 8, 'Status Update', 'Your application for \"Burger\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:39:29'),
(90, 8, 'Application Submitted', 'Your application for Kapehan Ni Juan has been submitted and is currently Pending.', 'info', 0, '2026-04-20 00:41:58'),
(92, 2, 'New Application', 'New application submitted: Kapehan Ni Juan (ID: 9)', 'info', 0, '2026-04-20 00:41:58'),
(94, 5, 'New Application', 'New application submitted: Kapehan Ni Juan (ID: 9)', 'info', 0, '2026-04-20 00:41:58'),
(95, 6, 'New Application', 'New application submitted: Kapehan Ni Juan (ID: 9)', 'info', 0, '2026-04-20 00:41:58'),
(98, 8, 'Status Update', 'Your application for \"Kapehan Ni Juan\" has been updated to: Under Review.', 'info', 0, '2026-04-20 00:42:16'),
(100, 8, 'Status Update', 'Your application for \"Kapehan Ni Juan\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:42:33'),
(102, 2, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Donut (ID: 7).', 'info', 0, '2026-04-20 00:53:11'),
(103, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:53:32'),
(105, 2, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Donut (ID: 7).', 'info', 0, '2026-04-20 00:54:10'),
(106, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:54:18'),
(108, 2, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Donut (ID: 7).', 'info', 0, '2026-04-20 00:58:05'),
(109, 8, 'Status Update', 'Your application for \"Donut\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 00:58:35'),
(111, 2, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Donut (ID: 7).', 'info', 0, '2026-04-20 01:00:59'),
(112, 8, 'Status Update', 'Your application for \"Burger\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:13:44'),
(114, 8, 'Status Update', 'Your application for \"Burger\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:17:18'),
(115, 1, 'Staff Update', 'Staff member (ID: 2) updated application Burger (ID: 8) to Approved.', 'info', 1, '2026-04-20 01:17:18'),
(116, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review.', 'info', 0, '2026-04-20 01:22:49'),
(117, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Under Review.', 'info', 1, '2026-04-20 01:22:49'),
(118, 7, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:23:11'),
(119, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 4) to Under Review.', 'info', 1, '2026-04-20 01:23:11'),
(120, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:24:32'),
(121, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Approved.', 'info', 1, '2026-04-20 01:24:32'),
(122, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:24:47'),
(123, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Under Review.', 'info', 1, '2026-04-20 01:24:47'),
(124, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Rejected. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:25:00'),
(125, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Rejected.', 'info', 1, '2026-04-20 01:25:00'),
(126, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:25:17'),
(127, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Under Review.', 'info', 1, '2026-04-20 01:25:17'),
(128, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:25:31'),
(129, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Returned for Correction.', 'info', 1, '2026-04-20 01:25:31'),
(130, 6, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Quick Fix Electronics (ID: 5).', 'info', 0, '2026-04-20 01:26:34'),
(131, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:26:50'),
(132, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Under Review.', 'info', 1, '2026-04-20 01:26:50'),
(133, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:27:03'),
(134, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Approved.', 'info', 1, '2026-04-20 01:27:03'),
(135, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 01:27:10'),
(136, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Ready for Pickup.', 'info', 1, '2026-04-20 01:27:10'),
(137, 9, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 01:27:59'),
(138, 6, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 01:48:52'),
(139, 6, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 1, '2026-04-20 01:49:09'),
(140, 5, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 01:54:18'),
(141, 10, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 02:03:28'),
(142, 13, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 02:17:45'),
(143, 14, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 02:25:11'),
(144, 8, 'Application Submitted', 'Your application for Sari Sari has been submitted and is currently Pending.', 'info', 0, '2026-04-20 02:26:54'),
(145, 1, 'New Application', 'New application submitted: Sari Sari (ID: 10)', 'info', 1, '2026-04-20 02:26:54'),
(146, 2, 'New Application', 'New application submitted: Sari Sari (ID: 10)', 'info', 0, '2026-04-20 02:26:54'),
(148, 8, 'Status Update', 'Your application for \"Sari Sari\" has been updated to: Under Review.', 'info', 0, '2026-04-20 02:27:22'),
(149, 1, 'Staff Update', 'Staff member (ID: 6) updated application Sari Sari (ID: 10) to Under Review.', 'info', 1, '2026-04-20 02:27:22'),
(150, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:27:37'),
(151, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Under Review.', 'info', 1, '2026-04-20 02:27:37'),
(152, 8, 'Status Update', 'Your application for \"Sari Sari\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:27:49'),
(153, 1, 'Staff Update', 'Staff member (ID: 6) updated application Sari Sari (ID: 10) to Approved.', 'info', 1, '2026-04-20 02:27:49'),
(154, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:32:07'),
(155, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Ready for Pickup.', 'info', 1, '2026-04-20 02:32:07'),
(156, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:35:00'),
(157, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Under Review.', 'info', 1, '2026-04-20 02:35:00'),
(158, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:35:08'),
(159, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Returned for Correction.', 'info', 1, '2026-04-20 02:35:08'),
(160, 6, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Quick Fix Electronics (ID: 5).', 'info', 0, '2026-04-20 02:36:38'),
(161, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Rejected. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:40:57'),
(162, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Rejected.', 'info', 1, '2026-04-20 02:40:57'),
(163, 2, 'New Assignment', 'A new application (ID: 4) has been assigned to you for review.', 'info', 0, '2026-04-20 02:41:17'),
(164, 2, 'New Assignment', 'A new application (ID: 3) has been assigned to you for review.', 'info', 0, '2026-04-20 02:41:26'),
(165, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:53:01'),
(166, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Ready for Pickup.', 'info', 1, '2026-04-20 02:53:01'),
(167, 8, 'Status Update', 'Your application for \"Quick Fix Electronics\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:53:53'),
(168, 1, 'Staff Update', 'Staff member (ID: 6) updated application Quick Fix Electronics (ID: 5) to Under Review.', 'info', 1, '2026-04-20 02:53:53'),
(169, 3, 'Status Update', 'Your application for \"Juan\'s Sari-Sari Store\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:54:00'),
(170, 1, 'Staff Update', 'Staff member (ID: 6) updated application Juan\'s Sari-Sari Store (ID: 1) to Returned for Correction.', 'info', 1, '2026-04-20 02:54:00'),
(171, 8, 'Status Update', 'Your application for \"Burger\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 0, '2026-04-20 02:54:20'),
(172, 1, 'Staff Update', 'Staff member (ID: 6) updated application Burger (ID: 8) to Ready for Pickup.', 'info', 1, '2026-04-20 02:54:20'),
(173, 16, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:41:09'),
(174, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:46:13'),
(175, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:46:27'),
(176, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:46:46'),
(177, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:47:03'),
(178, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:49:06'),
(179, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:51:14'),
(180, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:51:42'),
(181, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:56:10'),
(182, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 10:59:35'),
(183, 2, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 11:04:17'),
(184, 15, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-20 11:17:14'),
(185, 15, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-20 11:17:40'),
(186, 3, 'Application Submitted', 'Your application for Python ML Test Gas Station has been submitted and is currently Pending.', 'info', 0, '2026-04-20 12:00:23'),
(187, 1, 'New Application', 'New application submitted: Python ML Test Gas Station (ID: 11)', 'info', 1, '2026-04-20 12:00:23'),
(188, 2, 'New Application', 'New application submitted: Python ML Test Gas Station (ID: 11)', 'info', 0, '2026-04-20 12:00:23'),
(189, 15, 'New Application', 'New application submitted: Python ML Test Gas Station (ID: 11)', 'info', 0, '2026-04-20 12:00:23'),
(190, 8, 'Application Submitted', 'Your application for Test Business has been submitted and is currently Pending.', 'info', 0, '2026-04-20 12:20:36'),
(191, 1, 'New Application', 'New application submitted: Test Business (ID: 12)', 'info', 1, '2026-04-20 12:20:36'),
(192, 2, 'New Application', 'New application submitted: Test Business (ID: 12)', 'info', 0, '2026-04-20 12:20:36'),
(193, 15, 'New Application', 'New application submitted: Test Business (ID: 12)', 'info', 0, '2026-04-20 12:20:36'),
(194, 15, 'New Assignment', 'A new application (ID: 12) has been assigned to you for review.', 'info', 0, '2026-04-20 12:25:24'),
(195, 8, 'Status Update', 'Your application for \"Test Business\" has been updated to: Under Review.', 'info', 1, '2026-04-20 12:25:35'),
(196, 1, 'Staff Update', 'Staff member (ID: 15) updated application Test Business (ID: 12) to Under Review.', 'info', 1, '2026-04-20 12:25:35'),
(197, 8, 'Status Update', 'Your application for \"Test Business\" has been updated to: Returned for Correction. Staff Remarks: Updated by staff', 'info', 1, '2026-04-20 12:25:41'),
(198, 1, 'Staff Update', 'Staff member (ID: 15) updated application Test Business (ID: 12) to Returned for Correction.', 'info', 1, '2026-04-20 12:25:41'),
(199, 15, 'Correction Resubmitted', 'Applicant has resubmitted corrections for Test Business (ID: 12).', 'info', 0, '2026-04-20 12:27:33'),
(200, 17, 'Application Submitted', 'Your application for Fixed ML Gas Station has been submitted and is currently Pending.', 'info', 0, '2026-04-20 12:37:51'),
(201, 1, 'New Application', 'New application submitted: Fixed ML Gas Station (ID: 13)', 'info', 1, '2026-04-20 12:37:51'),
(202, 2, 'New Application', 'New application submitted: Fixed ML Gas Station (ID: 13)', 'info', 0, '2026-04-20 12:37:51'),
(203, 15, 'New Application', 'New application submitted: Fixed ML Gas Station (ID: 13)', 'info', 0, '2026-04-20 12:37:51'),
(204, 8, 'Application Submitted', 'Your application for Food Test has been submitted and is currently Pending.', 'info', 1, '2026-04-20 12:53:52'),
(205, 1, 'New Application', 'New application submitted: Food Test (ID: 14)', 'info', 1, '2026-04-20 12:53:52'),
(206, 2, 'New Application', 'New application submitted: Food Test (ID: 14)', 'info', 0, '2026-04-20 12:53:52'),
(207, 15, 'New Application', 'New application submitted: Food Test (ID: 14)', 'info', 0, '2026-04-20 12:53:52'),
(208, 15, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-20 13:26:16'),
(209, 15, 'New Assignment', 'A new application (ID: 8) has been assigned to you for review.', 'info', 1, '2026-04-20 13:27:27'),
(210, 8, 'Password Changed', 'Your password has been successfully reset.', 'success', 0, '2026-04-20 16:12:03'),
(211, 8, 'Password Changed', 'Your password has been successfully reset.', 'success', 0, '2026-04-20 16:23:01'),
(212, 18, 'Password Updated', 'Your permanent password has been successfully set.', 'success', 0, '2026-04-20 17:49:38'),
(213, 18, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-20 17:51:00'),
(214, 19, 'Password Updated', 'Your permanent password has been successfully set.', 'success', 0, '2026-04-20 18:08:11'),
(215, 19, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-20 18:08:26'),
(216, 19, 'Password Updated', 'Your permanent password has been successfully set.', 'success', 0, '2026-04-20 18:10:39'),
(217, 19, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-20 18:29:16'),
(218, 19, 'Password Updated', 'Your permanent password has been successfully set.', 'success', 0, '2026-04-20 18:29:52'),
(219, 18, 'New Assignment', 'A new application (ID: 13) has been assigned to you for review.', 'info', 0, '2026-04-21 18:17:55'),
(220, 19, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-21 18:18:32'),
(221, 18, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-21 18:18:44'),
(222, 19, 'New Assignment', 'A new application (ID: 13) has been assigned to you for review.', 'info', 0, '2026-04-21 18:18:54'),
(223, 17, 'Status Update', 'Your application for \"Fixed ML Gas Station\" has been updated to: Rejected. Staff Remarks: Updated by staff', 'info', 0, '2026-04-21 18:19:15'),
(224, 1, 'Staff Update', 'Staff member (ID: 19) updated application Fixed ML Gas Station (ID: 13) to Rejected.', 'info', 1, '2026-04-21 18:19:15'),
(225, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Under Review.', 'info', 0, '2026-04-21 23:22:21'),
(226, 1, 'Staff Update', 'Staff member (ID: 19) updated application Food Test (ID: 14) to Under Review.', 'info', 1, '2026-04-21 23:22:21'),
(227, 15, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-21 23:32:58'),
(228, 15, 'Password Updated', 'Your permanent password has been successfully set.', 'success', 0, '2026-04-21 23:33:15'),
(229, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Under Review.', 'info', 0, '2026-04-21 23:48:23'),
(230, 1, 'Staff Update', 'Staff member (ID: 15) updated application Food Test (ID: 14) to Under Review.', 'info', 1, '2026-04-21 23:48:23'),
(231, 3, 'Status Update', 'Your application for \"Juan\'s Sari-Sari Store\" has been updated to: Returned for Correction. Staff Remarks: Updated by staffokokok', 'info', 0, '2026-04-22 01:21:51'),
(232, 1, 'Staff Update', 'Staff member (ID: 15) updated application Juan\'s Sari-Sari Store (ID: 1) to Returned for Correction.', 'info', 0, '2026-04-22 01:21:51'),
(233, 3, 'Status Update', 'Your application for \"Python ML Test Gas Station\" has been updated to: Rejected. Staff Remarks: Updated by staff', 'info', 0, '2026-04-22 01:22:19'),
(234, 1, 'Staff Update', 'Staff member (ID: 15) updated application Python ML Test Gas Station (ID: 11) to Rejected.', 'info', 0, '2026-04-22 01:22:19'),
(235, 15, 'New Assignment', 'A new application (ID: 4) has been assigned to you for review.', 'info', 0, '2026-04-22 02:10:45'),
(236, 18, 'New Assignment', 'A new application (ID: 1) has been assigned to you for review.', 'info', 0, '2026-04-22 02:17:50'),
(237, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Under Review. Staff Remarks: failed', 'info', 0, '2026-04-22 04:22:49'),
(238, 1, 'Staff Update', 'Staff member (ID: 15) updated application Food Test (ID: 14) to Under Review.', 'info', 0, '2026-04-22 04:22:49'),
(239, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Rejected. Staff Remarks: Updated by staff', 'info', 0, '2026-04-22 04:23:35'),
(240, 1, 'Staff Update', 'Staff member (ID: 15) updated application Food Test (ID: 14) to Rejected.', 'info', 0, '2026-04-22 04:23:35'),
(241, 17, 'Status Update', 'Your application for \"Fixed ML Gas Station\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-29 17:29:06'),
(242, 1, 'Staff Update', 'Staff member (ID: 19) updated application Fixed ML Gas Station (ID: 13) to Under Review.', 'info', 0, '2026-04-29 17:29:06'),
(243, 19, 'New Assignment', 'A new application (ID: 14) has been assigned to you for review.', 'info', 0, '2026-04-29 17:31:05'),
(244, 19, 'New Assignment', 'A new application (ID: 11) has been assigned to you for review.', 'info', 0, '2026-04-29 17:31:08'),
(245, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 1, '2026-04-29 17:31:20'),
(246, 1, 'Staff Update', 'Staff member (ID: 19) updated application Food Test (ID: 14) to Under Review.', 'info', 0, '2026-04-29 17:31:20'),
(247, 8, 'Status Update', 'Your application for \"Kapehan Ni Juan\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 1, '2026-04-30 13:29:17'),
(248, 19, 'New Assignment', 'A new application (ID: 10) has been assigned to you for review.', 'info', 0, '2026-04-30 13:29:29'),
(249, 8, 'Application Submitted', 'Your Renewal application for Sari Sari has been submitted and is currently Pending.', 'info', 1, '2026-04-30 17:20:13'),
(250, 1, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 15)', 'info', 0, '2026-04-30 17:20:13'),
(251, 2, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 15)', 'info', 0, '2026-04-30 17:20:13'),
(252, 15, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 15)', 'info', 0, '2026-04-30 17:20:13'),
(253, 18, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 15)', 'info', 0, '2026-04-30 17:20:13'),
(254, 19, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 15)', 'info', 0, '2026-04-30 17:20:13'),
(257, 1, 'Application Submitted', 'Your Renewal application for Test has been submitted and is currently Pending.', 'info', 0, '2026-04-30 17:25:03'),
(258, 1, 'New Application', 'New Renewal application submitted: Test (ID: 16)', 'info', 0, '2026-04-30 17:25:03'),
(259, 2, 'New Application', 'New Renewal application submitted: Test (ID: 16)', 'info', 0, '2026-04-30 17:25:03'),
(260, 15, 'New Application', 'New Renewal application submitted: Test (ID: 16)', 'info', 0, '2026-04-30 17:25:03'),
(261, 18, 'New Application', 'New Renewal application submitted: Test (ID: 16)', 'info', 0, '2026-04-30 17:25:03'),
(262, 19, 'New Application', 'New Renewal application submitted: Test (ID: 16)', 'info', 0, '2026-04-30 17:25:03'),
(265, 8, 'Application Submitted', 'Your New application for Sari Sari has been submitted and is currently Pending.', 'info', 0, '2026-04-30 18:04:21'),
(266, 1, 'New Application', 'New New application submitted: Sari Sari (ID: 17)', 'info', 0, '2026-04-30 18:04:21'),
(267, 2, 'New Application', 'New New application submitted: Sari Sari (ID: 17)', 'info', 0, '2026-04-30 18:04:21'),
(268, 15, 'New Application', 'New New application submitted: Sari Sari (ID: 17)', 'info', 0, '2026-04-30 18:04:21'),
(269, 18, 'New Application', 'New New application submitted: Sari Sari (ID: 17)', 'info', 0, '2026-04-30 18:04:21'),
(270, 19, 'New Application', 'New New application submitted: Sari Sari (ID: 17)', 'info', 0, '2026-04-30 18:04:21'),
(273, 8, 'Status Update', 'Your application for \"Burger\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 18:06:06'),
(274, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 18:08:53'),
(275, 1, 'Staff Update', 'Staff member (ID: 19) updated application Food Test (ID: 14) to Approved.', 'info', 0, '2026-04-30 18:08:53'),
(276, 8, 'Application Submitted', 'Your Renewal application for Food Test has been submitted and is currently Pending.', 'info', 0, '2026-04-30 18:11:23'),
(277, 1, 'New Application', 'New Renewal application submitted: Food Test (ID: 18)', 'info', 0, '2026-04-30 18:11:23'),
(278, 2, 'New Application', 'New Renewal application submitted: Food Test (ID: 18)', 'info', 0, '2026-04-30 18:11:23'),
(279, 15, 'New Application', 'New Renewal application submitted: Food Test (ID: 18)', 'info', 0, '2026-04-30 18:11:23'),
(280, 18, 'New Application', 'New Renewal application submitted: Food Test (ID: 18)', 'info', 0, '2026-04-30 18:11:23'),
(281, 19, 'New Application', 'New Renewal application submitted: Food Test (ID: 18)', 'info', 0, '2026-04-30 18:11:23'),
(284, 8, 'Application Submitted', 'Your New application for SM Fairview has been submitted and is currently Pending.', 'info', 0, '2026-04-30 18:19:25'),
(285, 1, 'New Application', 'New New application submitted: SM Fairview (ID: 19)', 'info', 0, '2026-04-30 18:19:25'),
(286, 2, 'New Application', 'New New application submitted: SM Fairview (ID: 19)', 'info', 0, '2026-04-30 18:19:25'),
(287, 15, 'New Application', 'New New application submitted: SM Fairview (ID: 19)', 'info', 0, '2026-04-30 18:19:25'),
(288, 18, 'New Application', 'New New application submitted: SM Fairview (ID: 19)', 'info', 0, '2026-04-30 18:19:25'),
(289, 19, 'New Application', 'New New application submitted: SM Fairview (ID: 19)', 'info', 1, '2026-04-30 18:19:25'),
(292, 8, 'Status Update', 'Your application for \"Kapehan Ni Juan\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 18:20:24'),
(293, 1, 'Staff Update', 'Staff member (ID: 19) updated application Kapehan Ni Juan (ID: 9) to Approved.', 'info', 0, '2026-04-30 18:20:24'),
(294, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 18:34:55'),
(295, 1, 'Staff Update', 'Staff member (ID: 19) updated application Food Test (ID: 18) to Approved.', 'info', 0, '2026-04-30 18:34:55'),
(296, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 18:35:13'),
(297, 8, 'Application Submitted', 'Your Renewal application for Kapehan Ni Juan has been submitted and is currently Pending.', 'info', 0, '2026-04-30 18:45:52'),
(298, 1, 'New Application', 'New Renewal application submitted: Kapehan Ni Juan (ID: 20)', 'info', 0, '2026-04-30 18:45:52'),
(299, 2, 'New Application', 'New Renewal application submitted: Kapehan Ni Juan (ID: 20)', 'info', 0, '2026-04-30 18:45:52'),
(300, 15, 'New Application', 'New Renewal application submitted: Kapehan Ni Juan (ID: 20)', 'info', 0, '2026-04-30 18:45:52'),
(301, 18, 'New Application', 'New Renewal application submitted: Kapehan Ni Juan (ID: 20)', 'info', 0, '2026-04-30 18:45:52'),
(302, 19, 'New Application', 'New Renewal application submitted: Kapehan Ni Juan (ID: 20)', 'info', 1, '2026-04-30 18:45:52'),
(305, 8, 'Status Update', 'Your application for \"Sari Sari\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 18:47:14'),
(306, 1, 'Staff Update', 'Staff member (ID: 19) updated application Sari Sari (ID: 15) to Approved.', 'info', 1, '2026-04-30 18:47:14'),
(307, 8, 'Status Update', 'Your application for \"Sari Sari\" has been updated to: Approved. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 18:47:29'),
(308, 1, 'Staff Update', 'Staff member (ID: 19) updated application Sari Sari (ID: 17) to Approved.', 'info', 0, '2026-04-30 18:47:29'),
(309, 8, 'Status Update', 'Your application for \"Food Test\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 19:24:52'),
(310, 8, 'Status Update', 'Your application for \"Kapehan Ni Juan\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 19:34:33'),
(311, 1, 'Staff Update', 'Staff member (ID: 19) updated application Kapehan Ni Juan (ID: 20) to Under Review.', 'info', 0, '2026-04-30 19:34:33'),
(312, 8, 'Status Update', 'Your application for \"Kapehan Ni Juan\" has been updated to: Approved. Staff Remarks: haha', 'info', 0, '2026-04-30 19:35:04'),
(313, 1, 'Staff Update', 'Staff member (ID: 19) updated application Kapehan Ni Juan (ID: 20) to Approved.', 'info', 0, '2026-04-30 19:35:04'),
(314, 8, 'Status Update', 'Your application for \"Kapehan Ni Juan\" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 0, '2026-04-30 19:56:35'),
(315, 1, 'Staff Update', 'Staff member (ID: 19) updated application Kapehan Ni Juan (ID: 20) to Under Review.', 'info', 1, '2026-04-30 19:56:35'),
(316, 8, 'Application Submitted', 'Your Renewal application for Sari Sari has been submitted and is currently Pending.', 'info', 0, '2026-04-30 20:05:58'),
(317, 1, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 21)', 'info', 1, '2026-04-30 20:05:58'),
(318, 2, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 21)', 'info', 0, '2026-04-30 20:05:58'),
(319, 15, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 21)', 'info', 0, '2026-04-30 20:05:58'),
(320, 18, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 21)', 'info', 0, '2026-04-30 20:05:58'),
(321, 19, 'New Application', 'New Renewal application submitted: Sari Sari (ID: 21)', 'info', 0, '2026-04-30 20:05:58'),
(324, 8, 'Status Update', 'Your application for \"Sari Sari\" has been updated to: Ready for Pickup. Staff Remarks: Updated by staff', 'info', 1, '2026-04-30 20:14:32'),
(325, 1, 'Staff Update', 'Staff member (ID: 19) updated application Sari Sari (ID: 17) to Ready for Pickup.', 'info', 1, '2026-04-30 20:14:32'),
(326, 19, 'New Assignment', 'A new application (ID: 21) has been assigned to you for review.', 'info', 0, '2026-04-30 22:06:54'),
(327, 8, 'Application Submitted', 'Your New application for Cafe  has been submitted and is currently Pending.', 'info', 1, '2026-04-30 22:14:04'),
(328, 1, 'New Application', 'New New application submitted: Cafe  (ID: 22)', 'info', 1, '2026-04-30 22:14:04'),
(329, 2, 'New Application', 'New New application submitted: Cafe  (ID: 22)', 'info', 0, '2026-04-30 22:14:04'),
(330, 15, 'New Application', 'New New application submitted: Cafe  (ID: 22)', 'info', 0, '2026-04-30 22:14:04'),
(331, 18, 'New Application', 'New New application submitted: Cafe  (ID: 22)', 'info', 0, '2026-04-30 22:14:04'),
(332, 19, 'New Application', 'New New application submitted: Cafe  (ID: 22)', 'info', 0, '2026-04-30 22:14:04'),
(335, 8, 'Status Update', 'Your application for \"Cafe \" has been updated to: Under Review. Staff Remarks: Updated by staff', 'info', 1, '2026-04-30 22:44:05'),
(336, 1, 'Staff Update', 'Staff member (ID: 19) updated application Cafe  (ID: 22) to Under Review.', 'info', 0, '2026-04-30 22:44:05'),
(337, 19, 'New Assignment', 'A new application (ID: 22) has been assigned to you for review.', 'info', 0, '2026-04-30 22:58:59'),
(338, 19, 'New Assignment', 'A new application (ID: 9) has been assigned to you for review.', 'info', 0, '2026-04-30 23:07:42'),
(339, 22, 'Account Updated', 'Your account information has been updated by an administrator.', 'info', 0, '2026-04-30 23:08:51'),
(340, 22, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-30 23:09:42'),
(341, 22, 'Password Reset', 'Your account password has been reset by an administrator. Please secure your new login details.', 'warning', 0, '2026-04-30 23:09:48'),
(342, 22, 'Password Updated', 'Your permanent password has been successfully set.', 'success', 0, '2026-04-30 23:10:39');

-- --------------------------------------------------------

--
-- Table structure for table `password_resets`
--

CREATE TABLE `password_resets` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('applicant','staff','admin') DEFAULT 'applicant',
  `must_change_password` tinyint(1) DEFAULT 0,
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `verification_code` varchar(100) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `email`, `password`, `role`, `must_change_password`, `status`, `created_at`, `verification_code`, `is_verified`) VALUES
(1, 'Admin', 'User', 'admin@caloocan.gov.ph', '$2y$10$VH/br0Q/nMkniVOmQKCNJ.TtjFfKULdwJvh6BE6m7S7sMkOYOMNPu', 'admin', 0, 'Active', '2026-04-19 23:52:47', NULL, 1),
(2, 'Verified', 'Staff', 'staff@caloocan.gov.ph', '$2y$10$VH/br0Q/nMkniVOmQKCNJ.TtjFfKULdwJvh6BE6m7S7sMkOYOMNPu', 'staff', 0, 'Active', '2026-04-19 23:52:47', NULL, 1),
(3, 'Juan', 'Dela Cruz', 'juan@example.com', '$2y$10$VH/br0Q/nMkniVOmQKCNJ.TtjFfKULdwJvh6BE6m7S7sMkOYOMNPu', 'applicant', 0, 'Active', '2026-04-19 23:52:47', NULL, 1),
(5, 'Staff', '', 'staff1@caloocan.gov.ph', '$2y$10$VH/br0Q/nMkniVOmQKCNJ.TtjFfKULdwJvh6BE6m7S7sMkOYOMNPu', '', 0, 'Active', '2026-04-19 23:52:47', NULL, 1),
(6, 'Staff', 'Two', 'staff5@caloocan.gov.ph', '$2y$10$.i6IKPU8riIkP4javy6KwukCST.lKSgXWBvSVs4LvKD2jksdxpAZ6', '', 0, 'Active', '2026-04-19 23:52:47', NULL, 1),
(7, 'Mira', 'Applicant', 'mira@example.com', '$2y$10$VH/br0Q/nMkniVOmQKCNJ.TtjFfKULdwJvh6BE6m7S7sMkOYOMNPu', 'applicant', 0, 'Active', '2026-04-19 23:52:47', NULL, 1),
(8, 'Mira Juliana', 'Alcantara', 'mirajulianaa1006@gmail.com', '$2y$10$rojQ69WYKrvuUb.cNYbmluqDsVdiPXivIPbHnndzaWG77Bc6Q6qQK', 'applicant', 0, 'Active', '2026-04-19 23:58:50', NULL, 1),
(9, 'Staff', 'Two', 'stafftest@caloocan.gov.ph', '$2y$10$OGMmI2X8lirAYysDb0yzvufkKxbTXRNTjgTZNjRLU1KHaheqGImom', '', 0, 'Active', '2026-04-20 01:15:19', NULL, 1),
(10, 'Staff', 'Mira', 'staffmira@caloocan.gov.ph', '$2y$10$Wr4CRXpiI6qQqm7FEPFxzeh6HHKpSzc9yfMDWQAnU3DuWAP99Zq3y', '', 0, 'Active', '2026-04-20 02:02:53', NULL, 1),
(13, 'Staff', 'Test', 'test@caloocan.gov.ph', '$2y$10$q3rISSGgEYZ2RiWshZML4ONxqOu8QqDCdZhtgKM5MK.QNxJXqJmTW', '', 0, 'Active', '2026-04-20 02:14:00', NULL, 1),
(14, 'Staff Six', '', 'staff6@caloocan.gov.ph', '$2y$10$zAAm3D0RoxFgr8CptgxzCOp4kdDAH05MfWdUL81HA1cBIJf0.2Yjy', '', 0, 'Active', '2026-04-20 02:24:56', NULL, 1),
(15, 'Test', 'Staff', 'test2@caloocan.gov.ph', '$2y$10$fsNlDlvE8kNBBoSlHEYR..JZMpJCtJE0UiUKfz8eTxSMpFieTjlrm', 'staff', 0, 'Active', '2026-04-20 02:42:04', NULL, 1),
(16, 'Test3', '', 'test3@caloocan.gov.ph', '$2y$10$AfZwiWnXIrCsqVMqFGP1.O66nJIpytFhVXOx0utI7tKPwaP1revfC', '', 0, 'Active', '2026-04-20 10:40:43', NULL, 1),
(17, 'Test', 'User', 'test_user@example.com', '$2y$10$3BZtuQztfAHF9PFDy8eZX.54RXYG9QLNJeqXBDZ7Y/bB5mBXq/PZC', 'applicant', 0, 'Active', '2026-04-20 12:35:41', NULL, 1),
(18, 'Staff4', '', 'test4@caloocan.gov.ph', '$2y$10$y1ykW0uhxt/aRJRU2.B1weEHEwryMMuClH7q0q6aUQ3JKlKnGIuTm', 'staff', 0, 'Active', '2026-04-20 17:46:07', NULL, 1),
(19, 'Staff5', '', 'test5@caloocan.gov.ph', '$2y$10$K5SYL8XBOop2eMqS9QNajeg2OQ/3GX9QHV0zBi3TfiaiqG58KjP/W', 'staff', 0, 'Active', '2026-04-20 18:07:09', NULL, 1),
(20, 'jerard', 'domingo', 'jlsd@gmail.com', '$2y$10$.aZuxyWUqibB3vc0DUiWG.IBJc.GJUoxAoVl.tOX63588cjej2FDm', 'applicant', 0, 'Active', '2026-04-21 23:10:20', NULL, 1),
(22, 'Staff7', '', 'staff7@caloocan.gov.ph', '$2y$10$prWjP2HH8mwBvxTxnz4ANuOTP9k5gqIvGrQbCg5IpSiK1Jg7z4GpK', 'staff', 0, 'Active', '2026-04-30 23:08:32', NULL, 0),
(23, 'Juliana', 'Alcantara', 'mlalcantara6108qc@student.fatima.edu.ph', '$2y$10$ntYG8C04VZmvORCXvaueguzlLpHmqXHRZb858xUq.BFqmr/HQ6.UK', 'applicant', 0, 'Active', '2026-05-01 00:03:17', '160651', 0),
(24, 'Juliana', 'Alcantara', 'alcantaramira06@gmail.com', '$2y$10$cCXAAPfynxtJll1zANvl2u5z1Mjcb4og1Lj4tYqjgo3oeMgP5A/Xu', 'applicant', 0, 'Active', '2026-05-01 00:10:53', '655705', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fk_assigned_staff` (`assigned_to`);

--
-- Indexes for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `application_id` (`application_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `email` (`email`),
  ADD KEY `token` (`token`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `audit_logs`
--
ALTER TABLE `audit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=260;

--
-- AUTO_INCREMENT for table `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=343;

--
-- AUTO_INCREMENT for table `password_resets`
--
ALTER TABLE `password_resets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_assigned_staff` FOREIGN KEY (`assigned_to`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `fk_notification_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
