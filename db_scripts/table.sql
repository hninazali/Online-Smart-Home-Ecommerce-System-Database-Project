USE oshes;

CREATE TABLE admin(
adminID VARCHAR(16) NOT NULL UNIQUE,
name VARCHAR(128) NOT NULL,
password VARCHAR(40) NOT NULL,
gender ENUM('M', 'F') NOT NULL,
phoneNumber VARCHAR(8) NOT NULL,
PRIMARY KEY(adminID));

CREATE TABLE Customer(

customerID VARCHAR(16) NOT NULL UNIQUE,
name VARCHAR(128) NOT NULL,
email VARCHAR(30) NOT NULL UNIQUE,
password VARCHAR(40) NOT NULL,
address VARCHAR(200) NOT NULL,
phoneNumber VARCHAR(8) NOT NULL,
gender ENUM('M', 'F') NOT NULL,

PRIMARY KEY (customerID)
);

CREATE TABLE products (
productID MEDIUMINT NOT NULL,
model VARCHAR(10) NOT NULL, 
category VARCHAR(6)    NOT NULL,
warranty INT NOT NULL, 
cost INT NOT NULL,
price INT NOT NULL,
PRIMARY KEY (productID));


CREATE TABLE items(

itemID MEDIUMINT NOT NULL,
colour VARCHAR(10) NOT NULL,
factory VARCHAR(35) NOT NULL,
powerSupply VARCHAR(7) NOT NULL,
purchaseStatus ENUM('unsold', 'sold') NOT NULL,
productionYear VARCHAR(4) NOT NULL ,
customerID VARCHAR(16) NOT NULL,
productID MEDIUMINT NOT NULL,
 
PRIMARY KEY (itemID),
FOREIGN KEY (customerID) REFERENCES Customer(customerID),
FOREIGN KEY (productID) REFERENCES products(productID)
);
