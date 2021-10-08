CREATE TABLE request(
  requestID MEDIUMINT NOT NULL AUTO_INCREMENT,
  serviceFee Int NOT NULL DEFAULT 0,
  requestStatus ENUM('Submitted', 'Submitted and Waiting for payment', 'In progress', 'Approved', 'Canceled', 'Completed') NOT NULL,
  dateOfRequest Date NOT NULL,
  dateOfPayment Date,
  customerID VARCHAR(16) NOT NULL,
  
  PRIMARY KEY (requestID),
  FOREIGN KEY (customerID) REFERENCES customer(customerID)
);

INSERT INTO request (requestStatus, dateOfRequest, customerID) VALUES("Submitted", "2021-10-18", "brenda3");
INSERT INTO request (requestStatus, dateOfRequest, customerID, serviceFee) VALUES("In progress", "2021-09-21", "brenda3", 32);