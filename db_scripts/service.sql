CREATE TABLE service(
serviceID MEDIUMINT NOT NULL AUTO_INCREMENT,
serviceStatus ENUM('waiting for approval', 'in progress', 'completed') DEFAULT 'waiting for approval',
itemID MEDIUMINT NOT NULL,
requestID MEDIUMINT NOT NULL,
adminID VARCHAR(16),

PRIMARY KEY(serviceID),
FOREIGN KEY(itemID) REFERENCES item(itemID),
FOREIGN KEY(requestID) REFERENCES request(requestID),
FOREIGN KEY(adminID) REFERENCES admin(adminID)
);

INSERT INTO service (serviceStatus, itemID, requestID) VALUES("waiting for approval", 1, 1);
INSERT INTO service (serviceStatus, itemID, requestID) VALUES("waiting for approval", 1, 2);
