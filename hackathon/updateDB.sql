-- Add financial information to the users table
ALTER TABLE savings_app.users ADD COLUMN income DECIMAL(10, 2);
ALTER TABLE savings_app.users ADD COLUMN monthly_expenses DECIMAL(10, 2);
ALTER TABLE savings_app.users ADD COLUMN current_deposit DECIMAL(10, 2);

-- Add priority to the savings_goals table
ALTER TABLE savings_app.savings_goals ADD COLUMN priority INT DEFAULT 1;  -- Priority (1 is highest)
