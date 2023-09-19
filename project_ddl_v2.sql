DROP TABLE patientOrgan;
DROP TABLE patientBlood;
DROP TABLE patientAccident;
DROP TABLE patientDetails;
DROP TABLE organAvailability;
DROP TABLE organDonor;
DROP TABLE organ;
DROP TABLE donor;
DROP TABLE bloodAvailability;
DROP TABLE bloodGroup;
DROP TABLE accidentHospital;
DROP TABLE hospitalLocation;
DROP TABLE hospitalDetails;
DROP TABLE accidents;
DROP TABLE zipcodeDetails;



CREATE TABLE zipcodeDetails
	(zipcode			CHAR(11),
	state_name			VARCHAR(30),
	city				VARCHAR(30),
	county				VARCHAR(30),
	 PRIMARY KEY (zipcode)
	);

CREATE TABLE accidents
	(accident_id		CHAR(11),
	 severity		INTEGER,
	 accident_time		TIMESTAMP,
	 accident_latitude		FLOAT,
	 accident_longitude		FLOAT,
	 street				VARCHAR(100),
	 side				CHAR(1),
	 zipcode			CHAR(11),
	 PRIMARY KEY (accident_id),
	 FOREIGN KEY(zipcode) REFERENCES zipcodeDetails(zipcode) ON DELETE SET NULL
	);
	

CREATE TABLE hospitalDetails
	(hospital_id		CHAR(15),
	 hospital_name		VARCHAR(100),
	 address		VARCHAR(100),
	 zipcode			CHAR(11),
	 telephone			CHAR(15),
	 hospital_type		VARCHAR(30),
	 beds_available		INTEGER,
	 helipad		CHAR(1),
	 PRIMARY KEY (hospital_id)
	);
	
CREATE TABLE hospitalLocation
	(hospital_id		CHAR(15),
	 hospital_latitude		FLOAT,
	 hospital_longitude		FLOAT,
	 PRIMARY KEY (hospital_id),
	 FOREIGN KEY(hospital_id) REFERENCES hospitalDetails(hospital_id) ON DELETE CASCADE
	);
	

CREATE TABLE accidentHospital
	(accident_id		CHAR(11),
	 hospital_id		CHAR(15),
	 distance		FLOAT NOT NULL,
	 PRIMARY KEY (accident_id, hospital_id),
	 FOREIGN KEY(accident_id) REFERENCES accidents(accident_id) ON DELETE CASCADE,
	 FOREIGN KEY(hospital_id) REFERENCES hospitalDetails(hospital_id) ON DELETE CASCADE
	);



CREATE TABLE bloodGroup
	(blood_group_id		CHAR(1),
	 blood_group		VARCHAR(3),
	 PRIMARY KEY (blood_group_id)
	);
	

CREATE TABLE bloodAvailability
	(blood_group_id		CHAR(1),
	 hospital_id		CHAR(15),
	 quantity		FLOAT,
	 PRIMARY KEY (blood_group_id, hospital_id),
	 FOREIGN KEY(blood_group_id) REFERENCES bloodGroup(blood_group_id) ON DELETE CASCADE,
	 FOREIGN KEY(hospital_id) REFERENCES hospitalDetails(hospital_id) ON DELETE CASCADE
	);
	

CREATE TABLE donor
	(donor_id		CHAR(10),
	 name		VARCHAR(30),
	 age		INTEGER,
	 sex		CHAR(1),
	 address		VARCHAR(100),
	 zipcode		CHAR(11),
	 phone		CHAR(10),
	 PRIMARY KEY (donor_id)
	);


CREATE TABLE organ
	(organ_id		CHAR(2),
	 organ		VARCHAR(20),
	 PRIMARY KEY (organ_id)
	);

CREATE TABLE organDonor
	(organ_id		CHAR(2),
	 donor_id		CHAR(10),
	 PRIMARY KEY (organ_id, donor_id),
	 FOREIGN KEY(organ_id) REFERENCES organ(organ_id) ON DELETE CASCADE,
	 FOREIGN KEY(donor_id) REFERENCES donor(donor_id) ON DELETE CASCADE
	);

	
CREATE TABLE organAvailability
	(organ_id		CHAR(2),
	 hospital_id		CHAR(15),
	 quantity		FLOAT,
	 PRIMARY KEY (organ_id, hospital_id),
	 FOREIGN KEY(organ_id) REFERENCES organ(organ_id) ON DELETE CASCADE,
	 FOREIGN KEY(hospital_id) REFERENCES hospitalDetails(hospital_id) ON DELETE CASCADE
	);
	

CREATE TABLE patientDetails
	(patient_id		CHAR(10),
	 name		VARCHAR(30),
	 age		INTEGER,
	 sex		CHAR(1),
	 address		VARCHAR(100),
	 phone		CHAR(10),
	 blood_group		VARCHAR(3),
	 PRIMARY KEY (patient_id)
	);


CREATE TABLE patientAccident
	(patient_id		CHAR(10),
	 accident_id		CHAR(11),
	 hospital_id		CHAR(15),
	 PRIMARY KEY (patient_id, accident_id),
	 FOREIGN KEY(patient_id) REFERENCES patientDetails(patient_id) ON DELETE CASCADE,
	 FOREIGN KEY(accident_id, hospital_id) REFERENCES accidentHospital(accident_id, hospital_id) ON DELETE CASCADE
	);

	
CREATE TABLE patientBlood
	(patient_id		CHAR(10),
	 blood_group_id		CHAR(5),
	 quantity		FLOAT NOT NULL,
	 PRIMARY KEY (patient_id, blood_group_id),
	 FOREIGN KEY(patient_id) REFERENCES patientDetails(patient_id) ON DELETE CASCADE,
	 FOREIGN KEY(blood_group_id) REFERENCES bloodGroup(blood_group_id) ON DELETE CASCADE
	);

CREATE TABLE patientOrgan
	(patient_id		CHAR(10),
	 organ_id		CHAR(2),
	 quantity		INTEGER NOT NULL,
	 PRIMARY KEY (patient_id, organ_id),
	 FOREIGN KEY(patient_id) REFERENCES patientDetails(patient_id) ON DELETE CASCADE,
	 FOREIGN KEY(organ_id) REFERENCES organ(organ_id) ON DELETE CASCADE
	);
