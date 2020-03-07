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
	airDryer BOOL NOT NULL,
    airFreshener BOOL NOT NULL,
    autoDryer BOOL NOT NULL,
    autoPaperTowel BOOL NOT NULL,
    autoSink BOOL NOT NULL,
    autoToilet BOOL NOT NULL,
    babyChangeStation BOOL NOT NULL,
    babyPowder BOOL NOT NULL,
    bathroomAttendant  BOOL NOT NULL,
    bidet BOOL NOT NULL,
    bodyTowel BOOL NOT NULL,
    bodywash BOOL NOT NULL,
    brailleLabeling BOOL NOT NULL,
    callButton BOOL NOT NULL,
    coatHook BOOL NOT NULL,
    contraception BOOL NOT NULL,
    diapers BOOL NOT NULL,
    hygieneProducts BOOL NOT NULL,
    firstAid BOOL NOT NULL,
    fullBodyMirror BOOL NOT NULL,
    garbageCan BOOL NOT NULL,
    heatedSeat BOOL NOT NULL,
    lotion BOOL NOT NULL,
    moistTowelette BOOL NOT NULL,
    music BOOL NOT NULL,
    needleDisposal BOOL NOT NULL,
    paperSeatCovers BOOL NOT NULL,
    paperTowel BOOL NOT NULL,
    perfumeCologne BOOL NOT NULL,
    safetyRail BOOL NOT NULL,
    sauna BOOL NOT NULL,
    shampoo BOOL NOT NULL,
    shower BOOL NOT NULL,
    tissues BOOL NOT NULL,
    wheelChairAccess BOOL NOT NULL,
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
	username VARCHAR(25) UNIQUE NOT NULL,
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
	mapServiceID INT,
	overallRating FLOAT NOT NULL,
	bestRatingID INT NOT NULL,
	washroomCount INT NOT NULL,
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
	comment VARCHAR(100) NOT NULL,
	floor INT NOT NULL,
	gender VARCHAR(25) NOT NULL,
	urinalCount INT NOT NULL,
	stallCount INT NOT NULL,
	amenities INT NOT NULL,
	overallRating FLOAT NOT NULL,
	avgRatingsID INT NOT NULL,
	reviewCount INT NOT NULL,
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
	  REFERENCES washrooms(id),

	UNIQUE KEY (userID, washroomID)
);
