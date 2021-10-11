USE oshes;

CREATE TABLE Product (
	productID 		INT 			NOT NULL,
    category 		VARCHAR(6) 		NOT NULL, 
	model 			VARCHAR(10) 	NOT NULL, 
    price 			INT 			NOT NULL,
    warranty 		INT 	        NOT NULL, 
    cost 			INT 			NOT NULL,
    PRIMARY KEY (productID) );

CREATE TABLE Item (
	itemID 			VARCHAR(4) 		NOT NULL UNIQUE,
	color 			VARCHAR(10) 	NOT NULL,
	factory 		VARCHAR(35) 	NOT NULL,
	powerSupply 	VARCHAR(7) 		NOT NULL,
	purchaseStatus  ENUM("Unsold", "Sold") NOT NULL, 
	productionYear 	VARCHAR(4) 		NOT NULL,
	warrantyExpiry 	DATE,
    customerID 		VARCHAR(16), 
    productID 		INT 			NOT NULL,
    dateOfPurchase 	DATE,
	PRIMARY KEY (itemID), 
    FOREIGN KEY (customerID) REFERENCES Customer(customerID),
    FOREIGN KEY (productID) REFERENCES Product(productID) );
    
CREATE TABLE ServiceRequest (
	requestID 		INT 			NOT NULL AUTO_INCREMENT, 
	serviceFee 		INT,
	requestStatus 	VARCHAR(40),
	dateOfRequest 	DATE,
	itemID 			VARCHAR(4)  	NOT NULL,
	dateOfPayment 	DATE,
	-- adminID 		VARCHAR(40),
	PRIMARY KEY (requestID),
	FOREIGN KEY (itemID) REFERENCES Item(itemID));

CREATE TABLE Service(
	serviceStatus 	ENUM("waiting for approval", "in progress", "completed"),
    itemID 			VARCHAR(4)  	NOT NULL,
    requestID 		INT 			NOT NULL,
	adminID 		VARCHAR(40),
    FOREIGN KEY (itemID) REFERENCES Item(itemID),
    FOREIGN KEY (requestID) REFERENCES ServiceRequest(requestID)
	FOREIGN KEY (adminID) REFERENCES Admin(adminID));


