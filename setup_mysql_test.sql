-- Create db if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- create user if it doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- grant privileges foruser on test db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- grant priveleges for user on schema db
GRANT SELECT ON PRIVILEGES ON performance_schema.* TO 'hbnb_test'@'localhost';

-- push priveleges
FLUSH PRIVILEGES;

-- show grants for user
SHOW GRANTS FOR 'hbnb_test'@'localhost';