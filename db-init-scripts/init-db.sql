CREATE DATABASE IF NOT EXISTS baza;
USE baza;

CREATE TABLE IF NOT EXISTS images (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  date DATETIME NOT NULL,
  ip_address VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE USER 'hehe'@'%' IDENTIFIED BY 'hehe';
GRANT ALL PRIVILEGES ON baza.* TO 'hehe'@'%';
FLUSH PRIVILEGES;
