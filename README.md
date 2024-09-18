# super-savers-budget-app
Prototype for Savings App (Hackathon Project):
This savings app was developed as part of a hackathon with Cleo, where we introduced innovative savings features into the app. The project focused on improving users' ability to set, track, and dynamically prioritize savings goals. Our team finished third place in the competition. I contributed to both the front-end and back-end development, handling most of the core functionality.

Technology Stack:

Back-End: Flask, Python

Front-End: HTML, CSS, Jinja2 (Flask templating)

Database: MySQL

Scheduling: Manually triggered savings updates, with a simulation feature to prototype faster updates during the hackathon.

How It Works
- Users log in to the app.
- They can set savings goals and monitor their progress through the savings page.
- The app calculates a safe daily saving amount based on the user's financial info and distributes that across goals with higher priority going to more urgent goals.
- Users can manually simulate daily updates to prototype progress.
- All data is stored and retrieved dynamically from a MySQL database.
- This app was designed with user-friendliness in mind, providing a clear, visual way for users to track their savings progress over time.

Features and Pages
1. Login Page (/)
Users can log in with their credentials (username and password).
The system verifies the login details against the SQL database.
Upon successful login, users are redirected to the home page.

![image](https://github.com/user-attachments/assets/b4b9428a-9326-4693-bbba-062123f80444)

2. Home Page (/home)
Displays the user's financial information, including total income, monthly expenses, and current deposit.
Users can set new savings goals by entering a target amount, start date, and end date.
The financial information is retrieved from the database.
If the user's financial information is incomplete, they are prompted to update it in the profile page.

![image](https://github.com/user-attachments/assets/ca2017d6-7c1f-4055-8f7f-13641e806cb8)

4. Savings Page (/savings)
Displays the user's active savings goals.
For each goal, users can see the total saved amount vs. the target amount, along with a progress bar that visually represents savings progress.
The daily update button allows users to simulate daily savings and see how their goals progress.
The app calculates the proportional savings amount for each goal based on priority and available daily saving capacity.

![image](https://github.com/user-attachments/assets/4e72b015-05b1-454e-a1ef-c693cf714c8c)

Savings Algorithm:

The app calculates a dynamic daily saving for each user based on their financial situation. It considers the user's income, monthly expenses, and current deposit to determine a maximum daily saving limit, ensuring the user has enough money left over for expenses.

The daily saving is distributed proportionally across multiple goals, prioritizing goals that have closer deadlines or larger target amounts. This is achieved through a proportional priority system, where each goal's urgency is calculated and savings are allocated accordingly.

If the calculated daily savings exceed the user's maximum limit, the app redistributes the savings across the goals while keeping the user’s finances in balance.

5. Profile Page (/profile)
Users can update their financial information, including income, monthly expenses, and current deposit.
This information is critical for the app to calculate safe daily savings for goals.

![image](https://github.com/user-attachments/assets/be3b2eed-81c4-4090-ba15-a720da7706fe)

6. Milestones Page (/milestones)
Displays user milestones based on their savings progress. Part of the gamification aspect of the product rebranding.

![image](https://github.com/user-attachments/assets/52d8f7c9-fe82-4d74-ad47-3bdf6fc54565)

7. Achievements Page (/achievements)
Showcases achievements and progress the user has made in reaching savings goals. Additional gamification. Utilises expandable and collapsable UI components.
![image](https://github.com/user-attachments/assets/e10ae424-fc2f-4d4b-84d6-1c68095a774f)

11. Simulate Daily Savings Update (/update_savings)
This route is designed for testing purposes, allowing users to simulate daily updates every 30 seconds instead of waiting for actual daily updates.
Savings progress is updated, and priorities are dynamically adjusted based on how close each goal is to its deadline.
