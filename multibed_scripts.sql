-- Drop All Tables to clean database environmet

DROP TABLE IF EXISTS Files;
DROP TABLE IF EXISTS Studies;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS users_in;

-- Creating files table

CREATE TABLE Files (
	file_id INTEGER NOT NULL AUTO_INCREMENT, 
	file_name VARCHAR(255) NOT NULL, 
	file_path VARCHAR(512) NOT NULL, 
	file_size FLOAT, 
	file_type ENUM('bed', 'csv', 'txt') NOT NULL,
	uploaded_by INTEGER NOT NULL, 
	upload_date TIMESTAMP DEFAULT,
	description TEXT,
	study_id INTEGER,
	species TEXT NOT NULL,
	genome_release VARCHAR(20) NOT NULL,
	experiment_type TEXT,  
	PRIMARY KEY (file_id),
	FOREIGN KEY(uploaded_by) REFERENCES Users(user_id),
	FOREIGN KEY(study_id) REFERENCES Studies(study_id)
)ENGINE=InnoDB;

-- Creating Studies Table

CREATE TABLE Studies(
	study_id INTEGER NOT NULL AUTO_INCREMENT, 
	stduy_name VARCHAR(255) NOT NULL UNIQUE, 
	description TEXT(300),
	project_id INTEGER NOT NULL,
	PRIMARY KEY(study_id),
	FOREIGN KEY(project_id) REFERENCES Projects(project_id)
)ENGINE=InnoDB;

-- Creating Projects Table

CREATE TABLE Projects(
	 project_id INTEGER NOT NULL auto_increment,
	 project_name varchar(30),
	 description TEXT(300),
	 PRIMARY KEY (project_id)
)ENGINE = InnoDB;

-- Creating Users Table

CREATE table Users(
	 user_id INTEGER NOT NULL AUTO_INCREMENT,
	 username INTEGER NOT NULL,
	 email VARCHAR(255) NOT NULL,
	 password VARCHAR(50) NOT NULL,
	 urole ENUM('user','admin','guest'),
	 PRIMARY KEY(user_id)
)ENGINE = InnoDB;

-- Creating User-Project Relationship Table (many-to-many)

CREATE table users_in(
	 user_id INTEGER NOT NULL,
	 project_id INTEGER NOT NULL,
	 PRIMARY KEY(user_id, project_id),
	 FOREIGN KEY (user_id) REFERENCES Users (user_id),
	 FOREIGN KEY (project_id) REFERENCES Projects (project_id),
)ENGINE = InnoDB;

-- Creating table to store user information before registration approval

CREATE TABLE PendingUsers (
    pending_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    email VARCHAR(100),
    urole VARCHAR(20) DEFAULT 'guest',
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
