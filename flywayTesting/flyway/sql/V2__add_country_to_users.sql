-- flyway/sql/V2__add_country_to_users.sql
ALTER TABLE users
ADD COLUMN country VARCHAR(100);
