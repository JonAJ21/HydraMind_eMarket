CREATE TABLE users (
	user_id UUID,
	login VARCHAR(52),
	password VARCHAR(60),
	email VARCHAR(128),
	role VARCHAR(8),
	active BOOLEAN
);
