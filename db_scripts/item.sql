CREATE TABLE item(
itemID MEDIUMINT NOT NULL AUTO_INCREMENT,
colour VARCHAR(10) NOT NULL,
factory VARCHAR(35) NOT NULL,
powerSupply VARCHAR(7) NOT NULL,
purchaseStatus ENUM('unsold', 'sold') NOT NULL,
productionYear VARCHAR(4) NOT NULL,
customerID VARCHAR(16),
productID MEDIUMINT NOT NULL,
dateOfPurchase DATE,

PRIMARY KEY (itemID),
FOREIGN KEY (customerID) REFERENCES customer(customerID),
FOREIGN KEY (productID) REFERENCES product(productID)
);

INSERT INTO item (colour, factory, powerSupply, purchaseStatus, productionYear, productID, dateOfPurchase) VALUES("purple", "Malaysia", "Battery", "unsold", 2012, 003, "2021-10-10");