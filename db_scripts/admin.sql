CREATE TABLE admin(
adminID VARCHAR(16) NOT NULL UNIQUE,
name VARCHAR(128) NOT NULL,
password VARCHAR(40) NOT NULL,
gender ENUM('M', 'F') NOT NULL,
phoneNumber VARCHAR(8) NOT NULL,
PRIMARY KEY(adminID));

--INSERT INTO admin VALUES ("admin2", "Admin2", "password", "M", "5555");