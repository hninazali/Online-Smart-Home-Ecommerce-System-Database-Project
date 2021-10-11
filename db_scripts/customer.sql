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

--INSERT INTO customer VALUES("brenda3","Brenda3","brenda3@gmail.com","password","1 Street", "4444", "F");