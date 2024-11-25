
# HighSpenderTracker

This is a simple Flask-based web application that allows users to interact with a database that stores information about users, their spending, and high spenders. The API provides endpoints to retrieve and store data related to user spending and identify high spenders based on predefined thresholds.

## Features:
- **Total Spending per User:** Retrieve the total amount of money a specific user has spent.
- **Average Spending by Age Group:** Retrieve the average spending for different age groups.
- **Store High Spenders:** Add users to a high spenders list if their spending exceeds a certain threshold.

## Technologies:
- **Flask:** A lightweight Python web framework to build the API.
- **SQLite:** A simple database engine to store user information and spending data.

## API Endpoints:

1. **Get Total Spending for a User:**
   - **URL:** `/total_spent/<user_id>`
   - **Method:** `GET`
   - **Parameters:**
     - `user_id` (int): The ID of the user for which you want to retrieve the total spending.
   - **Response:**
     - Success: `{ "user_id": user_id, "total_spending": total_spending }`
     - Error (No spending found): `{ "message": "User has spent 0.00" }`
  
2. **Get Average Spending by Age Group:**
   - **URL:** `/average_spending_by_age`
   - **Method:** `GET`
   - **Response:**
     - Success: `{ "age_group": avg_spending }`
     - Example: `{ "18-24": 120.5, "25-30": 200.3, ... }`
  
3. **Add a High Spender:**
   - **URL:** `/write_high_spenders/<user_id>/<total_spending>`
   - **Method:** `POST` or `GET`
   - **Parameters:**
     - `user_id` (int): The ID of the user.
     - `total_spending` (float): The total spending amount of the user.
   - **Response:**
     - Success (User added to high spenders): `{ "message": "User data successfully inserted" }`
     - Error (Spending below threshold): `{ "message": "User spending does not meet threshold" }`
     - Error (User already exists in high spenders): `{ "message": "User already exists in high spenders" }`

## Database Structure:
The application uses an SQLite database with three tables:
1. **user_info:** Stores user details (ID, name, email, age).
2. **user_spending:** Records the money spent by users, linked to their `user_id`.
3. **high_spenders:** Stores users whose total spending exceeds a predefined threshold (1000).

## Installation:

1. Clone or download this repository to your local machine.
2. Install dependencies (Flask):
   ```bash
   pip install flask
   ```
3. Run the application:
   ```bash
   python app.py
   ```

4. The application will run locally at `http://127.0.0.1:5000/`.

## Database Initialization:
Upon first run, the app will initialize the database and create the necessary tables (`user_info`, `user_spending`, and `high_spenders`). This ensures that the app is ready to use immediately.

## Example Requests:

### 1. Get Total Spending for a User:
```bash
GET http://127.0.0.1:5000/total_spent/1
```
**Response:**
```json
{
  "user_id": 1,
  "total_spending": 500.00
}
```

### 2. Get Average Spending by Age Group:
```bash
GET http://127.0.0.1:5000/average_spending_by_age
```
**Response:**
```json
{
  "18-24": 150.50,
  "25-30": 200.00,
  "31-36": 250.75
}
```

### 3. Add a High Spender:
```bash
POST http://127.0.0.1:5000/write_high_spenders/2/1500
```
**Response:**
```json
{
  "message": "User data successfully inserted"
}
```

---

## License:
This project is open source and available under the MIT License.

---

This README provides a quick overview of how to interact with the API, install it, and use its features. Let me know if you'd like any more changes!
