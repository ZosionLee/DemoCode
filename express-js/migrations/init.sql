-- MySQL Script generated by MySQL Workbench
-- Mon Oct 28 17:11:54 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- -----------------------------------------------------
-- Table `users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `users` ;

CREATE TABLE IF NOT EXISTS `users` (
  `id` CHAR(32) NOT NULL COMMENT 'user id, use uuid',
  `name` VARCHAR(128) NOT NULL COMMENT 'user name',
  `password` VARCHAR(256) NOT NULL COMMENT 'user password',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT 'created time',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT 'updated time',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_bin
COMMENT = 'user table';

-- -----------------------------------------------------
-- Table `Authors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `authors` ;

CREATE TABLE IF NOT EXISTS `authors` (
  `id` CHAR(32) NOT NULL COMMENT 'author id, use uuid',
  `name` VARCHAR(128) NOT NULL COMMENT 'author name',
  `age` INT NOT NULL COMMENT 'author age',
  `country` VARCHAR(64) NULL COMMENT 'author country',
  `qualification` JSON NULL COMMENT 'author qualification',
  `description` VARCHAR(512) NULL COMMENT 'author description',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT 'created time',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT 'updated time',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_bin
COMMENT = 'author table';


-- -----------------------------------------------------
-- Table `category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `categories` ;

CREATE TABLE IF NOT EXISTS `categories` (
  `id` CHAR(32) NOT NULL COMMENT 'category id, use uuid',
  `name` VARCHAR(128) NOT NULL COMMENT 'category name',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT 'created time',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT 'updated time',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_bin
COMMENT = 'category table';


-- -----------------------------------------------------
-- Table `publisher`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `publishers` ;

CREATE TABLE IF NOT EXISTS `publishers` (
  `id` CHAR(32) NOT NULL COMMENT 'publisher id, use uuid',
  `name` VARCHAR(128) NOT NULL COMMENT 'publisher name',
  `address` VARCHAR(1204) NOT NULL COMMENT 'publisher address',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT 'created time',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT 'updated time',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_bin
COMMENT = 'publisher table';

-- -----------------------------------------------------
-- Table `Books`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `books` ;

CREATE TABLE IF NOT EXISTS `books` (
  `id` CHAR(32) NOT NULL COMMENT 'book id, use uuid',
  `title` VARCHAR(128) NOT NULL COMMENT 'book name',
  `price` FlOAT NOT NULL COMMENT 'book age',
  `rank` INT NULL COMMENT 'book country',
  `description` VARCHAR(512) NULL COMMENT 'book description',
  `author_id` CHAR(32) NULL COMMENT 'author id',
  `category_id` CHAR(32) NULL COMMENT 'category id',
  `publisher_id` CHAR(32) NULL COMMENT 'publisher id',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT 'created time',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT 'updated time',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_bin
COMMENT = 'book table';

-- -----------------------------------------------------
-- Table `store`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `stories` ;

CREATE TABLE IF NOT EXISTS `stories` (
  `id` CHAR(32) NOT NULL COMMENT 'store id, use uuid',
  `name` VARCHAR(128) NOT NULL COMMENT 'store name',
  `address` VARCHAR(1204) NOT NULL COMMENT 'store address',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT 'created time',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT 'updated time',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_bin
COMMENT = 'store table';

-- -----------------------------------------------------
-- Table `book_store_relation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `book_store_relation` ;

CREATE TABLE IF NOT EXISTS `book_store_relation` (
  `id` CHAR(32) NOT NULL COMMENT 'uuid',
  `book_id` VARCHAR(128) NOT NULL COMMENT 'book id',
  `store_id` VARCHAR(1204) NOT NULL COMMENT 'store id',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT 'created time',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT 'updated time',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_bin
COMMENT = 'bookstore table';