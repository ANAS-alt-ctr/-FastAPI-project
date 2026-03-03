Project Overview

This is a basic FastAPI application built with Python that:

Stores and reads user data from a JSON file (users.json)

Provides multiple API endpoints to list, add, delete, and analyze users

Performs analysis on user reviews (word count, uppercase letters, special characters)

The entire app runs using FastAPI, and data persistence is done using a local JSON file.

Features & Endpoints
Root Endpoint
GET /

Returns all users from users.json.

List Users with Pagination & Sorting
GET /users?limit=<int>&offset=<int>&sort=<asc|desc>

Responds with a list of users
Supports query parameters:

limit – how many users to return

offset – how many to skip

sort – order by id ascending or descending

Create a New User
POST /users

Accepts JSON body with:

name

age

city

email

review (text)

Stores new user in the JSON file
Automatically computes review analysis (word count, uppercase letters, special characters) and appends it to the user object.

Delete a User
DELETE /users/{user_id}

Removes a user with a matching id
Returns a success message or 404 if not found.

Analyze a User’s Review
GET /Analyze/{user_id}

Computes review metrics (if not present)
Returns:

word count

uppercase letters count

special characters count
Each analysis also has its own UUID-like counter.

 Retrieve User Analyses
GET /users/{user_id}/analyses

Optional query filters:

limit – number of analysis results

offset – skip first N analyses

sort – ascending/descending

min_words – only show analyses where word count ≥ this number
Returns sorted and filtered list of analyses.

 Data File

users.json — stores all user data in JSON format.
This file is read on startup and updated when users are created or deleted.

Data Validation

Uses Pydantic models to validate incoming user data (including email format).

Review must be non‑empty and ≤ 200 characters.

🛠 Running the Project

Basic steps (assumed):

Install dependencies:

pip install fastapi uvicorn

Run the app:

uvicorn main:app --reload

Test endpoints on http://localhost:8000/docs

(Automatic interactive API docs are available because of FastAPI’s OpenAPI integration.)

 Summary
Feature	Supported
List users
Pagination & sorting
Create user
Delete user
Analyze review
Analysis filters
JSON storage	

error info:
I face the errors : 
1. In the save the Analysis data in json
2. In the GET Parameters in sort
3. In Analysis the its show Empty data
4. Some time the Analysis uid is Generating
