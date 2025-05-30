-- Create table to store user information before registration approval

CREATE TABLE PendingUsers (
    pending_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    email VARCHAR(100),
    urole VARCHAR(20) DEFAULT 'guest',
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
