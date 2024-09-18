-- Replace 'flask_user' with the username you want to use
-- Replace 'your_flask_password' with the password for that user

CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'your_flask_password';

-- Grant all privileges to this user for your `savings_app` database
GRANT ALL PRIVILEGES ON savings_app.* TO 'flask_user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

