# Assume that a database has already been specified (in this case just "db")

create table ratings(
	id INT NOT NULL AUTO_INCREMENT,
	cleanliness FLOAT NOT NULL,
	privacy FLOAT NOT NULL,
	smell FLOAT NOT NULL,
	toiletPaperQuality FLOAT NOT NULL,
	PRIMARY KEY (id)
);


create table amenities(
	id INT NOT NULL AUTO_INCREMENT,
	paperTowel BOOL NOT NULL,
	airDryer BOOL NOT NULL,
	soap BOOL NOT NULL,
	wheelChairAccess BOOL NOT NULL,
	autoSink BOOL NOT NULL,
	autoToilet BOOL NOT NULL,
	autoPaperTowel BOOL NOT NULL,
	autoDryer BOOL NOT NULL,
	shower BOOL NOT NULL,
	urinal BOOL NOT NULL,
	paperSeatCovers BOOL NOT NULL,
	hygieneProducts BOOL NOT NULL,
	needleDisposal BOOL NOT NULL,
	contraceptives BOOL NOT NULL,
	bathroomAttendant BOOL NOT NULL,
	perfume BOOL NOT NULL,
	lotion BOOL NOT NULL,
	PRIMARY KEY (id)
);


create table preferences(
	id INT NOT NULL AUTO_INCREMENT,
	gender VARCHAR(25) NOT NULL,
	wheelchairAccess BOOL NOT NULL,
	mainFloorAccess BOOL NOT NULL,
	PRIMARY KEY (id)
);


create table users(
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(25) NOT NULL,
	created TIMESTAMP NOT NULL,
	profilePic TEXT,
	preferences INT NOT NULL,

	PRIMARY KEY (id),

	FOREIGN KEY (preferences)
	  REFERENCES preferences(id)
);


create table buildings(
	id INT NOT NULL AUTO_INCREMENT,
	created TIMESTAMP NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	title VARCHAR(100) NOT NULL,
	mapServiceID VARCHAR(100),
	overallRating FLOAT NOT NULL,
	bestRatingID INT NOT NULL,
	PRIMARY KEY (id),

	FOREIGN KEY (bestRatingID)
	  REFERENCES ratings(id)
);


create table washrooms(
	id INT NOT NULL AUTO_INCREMENT,
	created TIMESTAMP NOT NULL,
	buildingID INT NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	title VARCHAR(100) NOT NULL,
	floor INT NOT NULL,
	gender VARCHAR(25) NOT NULL,
	amenities INT NOT NULL,
	overallRating FLOAT NOT NULL,
	avgRatingsID INT NOT NULL,
	PRIMARY KEY (id),

	FOREIGN KEY (buildingID)
	  REFERENCES buildings(id),

    FOREIGN KEY (amenities)
      REFERENCES amenities(id),

	FOREIGN KEY (avgRatingsID)
	  REFERENCES ratings(id)
);


create table reviews(
	id INT NOT NULL AUTO_INCREMENT,
	created TIMESTAMP NOT NULL,
	washroomID INT NOT NULL,
	user INT NOT NULL,
	ratingID INT NOT NULL,
	comment TEXT NOT NULL,
	upvoteCount INT NOT NULL,
	PRIMARY KEY (id),

	FOREIGN KEY (washroomID)
	  REFERENCES washrooms(id),

	FOREIGN KEY (user)
	  REFERENCES users(id),

	FOREIGN KEY (ratingID)
	  REFERENCES ratings(id)
);


create table favorites(
	id INT NOT NULL AUTO_INCREMENT,
	userID INT NOT NULL,
	washroomID INT NOT NULL,
	PRIMARY KEY (id),

	FOREIGN KEY (userID)
	  REFERENCES users(id),

	FOREIGN KEY (washroomID)
	  REFERENCES washrooms(id)
);