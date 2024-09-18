from flask import Flask, redirect, url_for, render_template, request, session, Response
import time
import mysql.connector
from datetime import date
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="flask_user",  # Replace with your MySQL user
    password="your_flask_password",  # Replace with your MySQL password
    database="savings_app"
)

cursor = db.cursor()

# ---------------------------------
# Login Route (SQL Integration)
# ---------------------------------
@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['login1']
        password = request.form['password']

        # Check the username and password from the database
        cursor.execute("SELECT id, username FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for("home"))
        else:
            return "Login failed. Invalid username or password."
    else:
        return render_template('login.html')

# ---------------------------------
# Home Route (Capture Financial Info and Create Savings Goal)
# ---------------------------------
@app.route('/home', methods=["POST", "GET"])
def home():
    user = session.get('username')
    if not user:
        return redirect(url_for('login'))

    user_id = session.get('user_id')

	# Fetch user's financial info from the database
    cursor.execute("SELECT total_saved, income, monthly_expenses, current_deposit FROM users WHERE id=%s", (user_id,))
    financial_info = cursor.fetchone()


    if financial_info:
        total_saved, income, monthly_expenses, current_deposit = financial_info
    else:
        total_saved, income, monthly_expenses, current_deposit = None, None, None, None
        

	
    if request.method == "POST":
        
        # Financial Info
        #income = request.form['income']
        #monthly_expenses = request.form['monthly_expenses']
        #current_deposit = request.form['current_deposit']
        
		

        # Savings Goal Info
        item = request.form['home1']
        target_amount = request.form['home2']
        start_date = request.form['home3']
        end_date = request.form['home4']

        # Update user's financial info in the database
        #cursor.execute("UPDATE users SET income=%s, monthly_expenses=%s, current_deposit=%s WHERE id=%s", 
        #               (income, monthly_expenses, current_deposit, user_id))
        #db.commit()

        # Insert savings goal into the database
        cursor.execute(
            "INSERT INTO savings_goals (user_id, item, target_amount, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
            (user_id, item, target_amount, start_date, end_date)
        )
        db.commit()

        return redirect(url_for("savings"))
    else:
        return render_template('home.html', username=user, 
                               income=income, 
                               monthly_expenses=monthly_expenses, 
                               current_deposit=current_deposit,
                               total_saved =total_saved)
							   #income=session.get('income'), 
                               #monthly_expenses=session.get('monthly_expenses'), 
                               #current_deposit=session.get('current_deposit'))
# ---------------------------------
# Savings Page: Display Goals and Progress
# ---------------------------------
@app.route('/savings')
def savings():
    user_id = session.get('user_id')
    user = session.get('username')
    if not user_id:
        return redirect(url_for('login'))

    # Fetch savings goals from the database
    cursor.execute("SELECT item, target_amount, saved_amount, start_date, end_date FROM savings_goals WHERE user_id=%s", (user_id,))
    savings_goals = cursor.fetchall()

    # Calculate progress percentages for each savings goal
    goals_with_progress = []
    for goal in savings_goals:
        item, target_amount, saved_amount, start_date, end_date = goal
        progress_percentage = (saved_amount / target_amount) * 100 if target_amount and saved_amount else 0
        goals_with_progress.append((item, target_amount, saved_amount, start_date, end_date, progress_percentage))

    # Pass these goals with progress to the template
    return render_template('savings.html', username=user, savings_goals=goals_with_progress)

# ---------------------------------
# Profile Route (Update Financial Info)
# ---------------------------------
@app.route('/profile', methods=["POST", "GET"])
def profile():
    user = session.get('username')
    if not user:
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    if request.method == "POST":
        income = request.form['income']
        monthly_expenses = request.form['monthly_expenses']
        current_deposit = request.form['current_deposit']

        # Update financial info in the database
        cursor.execute("UPDATE users SET income=%s, monthly_expenses=%s, current_deposit=%s WHERE id=%s", 
                       (income, monthly_expenses, current_deposit, user_id))
        db.commit()

        # Update session variables
        session['income'] = income
        session['monthly_expenses'] = monthly_expenses
        session['current_deposit'] = current_deposit

        return redirect(url_for("home"))
    else:
        return render_template('profile.html', income=session.get('income'), 
                               monthly_expenses=session.get('monthly_expenses'), 
                               current_deposit=session.get('current_deposit'))

# ---------------------------------
# Milestones Route
# ---------------------------------
@app.route('/milestones')
def milestones():
    user = session.get('username')
    if not user:
        return redirect(url_for('login'))
    return render_template('milestones.html')

# ---------------------------------
# Achievements Route
# ---------------------------------
@app.route('/achievements')
def achievements():
    user = session.get('username')
    if not user:
        return redirect(url_for('login'))
    return render_template('achievements.html')

# ---------------------------------
# Logout Route
# ---------------------------------
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    session.pop('user_id', None)   # Remove user ID from session
    return redirect(url_for('login'))

# ---------------------------------
# Real-time Progress Bars Using SSE (Server-Sent Events)
# ---------------------------------
@app.route('/progress1')
def progress1():
    def generate_progress1():
        progress = 0
        while progress < 100:
            progress += 10
            time.sleep(1)
            yield f"data:{progress}\n\n"
    return Response(generate_progress1(), mimetype='text/event-stream')

@app.route('/progress2')
def progress2():
    def generate_progress2():
        progress = 0
        while progress < 100:
            progress += 20
            time.sleep(1.5)
            yield f"data:{progress}\n\n"
    return Response(generate_progress2(), mimetype='text/event-stream')


# THIS IS THE BIT YOU WROTE BELOW THAT IS WRONG AND NEEDS CHANGING 
# I THINK EVERYTHING ELSE IS FINE BUT I MIGHT BE WRONG.
# IF YOU UNDERSTAND THIS COMMENTS ABOVE THEN COMMENT YES BELOW:



def update_daily_savings():
    # Get the current logged-in user's ID from the session
    user_id = session.get('user_id')

    # Fetch user's financial info
    cursor.execute("SELECT income, monthly_expenses, current_deposit FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if not user:
        return  # If no user found, stop the function
    
    income, monthly_expenses, current_deposit = user
    
    # Calculate the max daily saving the user can afford
    max_daily_save = (income - monthly_expenses) / 30
    
    # Fetch savings goals for this user
    cursor.execute("SELECT id, target_amount, saved_amount, start_date, end_date FROM savings_goals WHERE user_id=%s", (user_id,))
    goals = cursor.fetchall()

    if not goals:
        return  # No goals for this user

    # Calculate priorities dynamically based on time left and amount left to save
    total_priority_score = 0
    goal_data = []

    for goal in goals:
        goal_id, target_amount, saved_amount, start_date, end_date = goal
        days_left = (end_date - datetime.now().date()).days
        if days_left <= 0:
            continue  # Skip if the deadline has passed

        amount_left = target_amount - saved_amount
        priority = amount_left / days_left  # Proportional priority calculation

        total_priority_score += priority
        goal_data.append({
            "goal_id": goal_id,
            "priority": priority,
            "amount_left": amount_left,
            "days_left": days_left,
        })

    # Distribute daily savings based on proportional priority
    for goal in goal_data:
        proportional_priority = goal["priority"] / total_priority_score
        daily_saving = proportional_priority * max_daily_save  # Dynamic daily saving based on priority

        # Apply daily savings and update the database
        cursor.execute(
            "UPDATE savings_goals SET saved_amount = saved_amount + %s, last_saved_time = %s WHERE id = %s",
            (daily_saving, datetime.now(), goal["goal_id"])
        )
        db.commit()

    # Update total saved across all goals for the user
    cursor.execute("SELECT SUM(saved_amount) FROM savings_goals WHERE user_id=%s", (user_id,))
    total_saved = cursor.fetchone()[0] or 0

    # Update total saved in the users table
    cursor.execute("UPDATE users SET total_saved = %s WHERE id = %s", (total_saved, user_id))
    db.commit()

        
# Route to trigger the daily savings update manually (for testing)
@app.route('/update_savings')
def manual_update_savings():
    update_daily_savings()
    return redirect(url_for('savings'))
    #return "Daily savings updated!"

# END OF FAULTY CODE YOU WROTE
# To auto-update the website without needing to rerun the file
if __name__ == "__main__":
    app.run(debug=True)
