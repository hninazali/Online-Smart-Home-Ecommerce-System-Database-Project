CREATE TABLE customer(

customerID MEDIUMINT NOT NULL AUTO_INCREMENT,
name VARCHAR(40) NOT NULL,
email VARCHAR(30) NOT NULL UNIQUE,
password VARCHAR(128) NOT NULL,
address VARCHAR(200) NOT NULL,
phoneNumber VARCHAR(8) NOT NULL,
gender ENUM('F', 'M') NOT NULL,

PRIMARY KEY (customerID)
);