CREATE TABLE request(
  requestID MEDIUMINT NOT NULL AUTO_INCREMENT,
  serviceFee INT NOT NULL DEFAULT 0,
  requestStatus ENUM('Submitted', 'Submitted and Waiting for payment', 'In progress', 'Approved', 'Canceled', 'Completed') NOT NULL,
  dateOfRequest DATE NOT NULL,
  dateOfPayment DATE,
  customerID VARCHAR(16) NOT NULL,
  itemID MEDIUMINT NOT NULL,
  
  PRIMARY KEY (requestID),
  FOREIGN KEY (customerID) REFERENCES customer(customerID),
  FOREIGN KEY (itemID) REFERENCES item(itemID)
);

--INSERT INTO request (requestStatus, dateOfRequest, customerID, itemID) VALUES("Submitted", "2021-10-18", "brenda3", 1);
--INSERT INTO request (requestStatus, dateOfRequest, customerID, serviceFee, itemID) VALUES("In progress", "2021-09-21", "brenda3", 32, 1);