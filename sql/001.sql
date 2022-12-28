\c fibonacci

CREATE TABLE fibonacci (
	id SERIAL NOT NULL,
	ordinal INTEGER NOT NULL,
	nth INTEGER NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (ordinal)
);