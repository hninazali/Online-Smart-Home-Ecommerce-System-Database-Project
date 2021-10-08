CREATE TABLE product(
productID MEDIUMINT NOT NULL,
model VARCHAR(10) NOT NULL, 
category VARCHAR(6) NOT NULL,
warranty INT NOT NULL, 
cost INT NOT NULL,
price INT NOT NULL,

PRIMARY KEY (productID) 
);

INSERT INTO product VALUES(003, "SmartHome1", "Lights", 8, 30.0, 70.0);