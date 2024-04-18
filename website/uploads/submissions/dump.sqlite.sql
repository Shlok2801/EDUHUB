-- TABLE
CREATE TABLE assignment (
	id INTEGER NOT NULL, 
	data VARCHAR(1000000000000000000000000000000), 
	assign_date DATETIME, 
	creator INTEGER, 
	file VARCHAR(150), 
	course_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(creator) REFERENCES user (id), 
	FOREIGN KEY(course_id) REFERENCES course (id)
);
CREATE TABLE course (
	id INTEGER NOT NULL, 
	name VARCHAR(100), 
	description VARCHAR(100), 
	creator INTEGER, 
	enroll_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(creator) REFERENCES user (id)
);
CREATE TABLE discussion (
	id INTEGER NOT NULL, 
	message VARCHAR(1000), 
	course_id INTEGER, 
	user_id INTEGER, 
	timestamp DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(course_id) REFERENCES course (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE enroll (
	id INTEGER NOT NULL, 
	course_id INTEGER, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(course_id) REFERENCES course (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE material (
	id INTEGER NOT NULL, 
	message VARCHAR(1000), 
	course_id INTEGER, 
	description VARCHAR(100), 
	timestamp DATETIME, 
	file VARCHAR(150), 
	PRIMARY KEY (id), 
	FOREIGN KEY(course_id) REFERENCES course (id)
);
CREATE TABLE notification (
	id INTEGER NOT NULL, 
	course_id INTEGER, 
	user_id INTEGER, 
	message VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(course_id) REFERENCES course (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE submission (
	id INTEGER NOT NULL, 
	assignment_id INTEGER, 
	submitter INTEGER, 
	description VARCHAR(100), 
	timestamp DATETIME, 
	file VARCHAR(150), 
	PRIMARY KEY (id), 
	FOREIGN KEY(assignment_id) REFERENCES assignment (id), 
	FOREIGN KEY(submitter) REFERENCES user (id)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	email VARCHAR(150), 
	password VARCHAR(150), 
	first_name VARCHAR(150), 
	last_name VARCHAR(150), 
	role VARCHAR(150), 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
 
-- INDEX
 
-- TRIGGER
 
-- VIEW
 
