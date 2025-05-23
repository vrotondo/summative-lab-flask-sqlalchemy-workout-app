Summative Lab: Flask SQLAlchemy Workout Application Backend
This summative lab is your opportunity to bring together everything you've learned throughout this course. You'll design and build a complete backend API for a workout application. Using Flask, SQLAlchemy, and Marshmallow, you’ll define models and relationships, enforce constraints and validations, seed data, and create endpoints for common API tasks. By working through this open-ended lab, you’ll demonstrate your ability to implement robust, real-world backend systems that follow professional standards.

Scenario

Your team is developing a backend API for a workout tracking application used by personal trainers. The API will be responsible for tracking workouts and their associated exercises. Each workout can include multiple exercises, with sets, reps, or duration attached to each. Exercises need to be reusable so a trainer can add the same exercise to various workouts. You’ve received a spec that outlines the models, relationships, and required endpoints. You are responsible for building a clean, maintainable, and validated backend that meets this spec.

By completing this lab, you will:

Practice building a backend architecture from scratch using Flask and SQLAlchemy.
Apply all forms of validations to ensure clean and consistent data.
Use Marshmallow schemas to serialize complex relationships and ensure request integrity.
Define models, migrations, and seed data for a multi-table relational schema.
Build API endpoints aligned with REST conventions and real-world use cases.
Gain confidence managing app structure, commits, and GitHub repo organization.
Tools and Resources
Python 3.8.13+
Text Editor or IDE (e.g., VS Code)
Git + GitHub
Pipenv
The following Python packages (for your Pipfile):
Flask = "2.2.2"
Flask-Migrate = "3.1.0"
flask-sqlalchemy = "3.0.3"
Werkzeug = "2.2.2"
importlib-metadata = "6.0.0"
importlib-resources = "5.10.0"
ipdb = "0.13.9"
marshmallow = "3.20.1"

Instructions

Task 1: Define the Problem
Design an API that enables:

Creation, deletion, and viewing of workouts.
Creation, deletion, and viewing of Exercises.
Adding exercise to a workout.
Note, for this application you do not need to implement any update actions. You also do not need to allow a user to remove an exercise from a workout, just add one.

Your API should have validations on the model and schema level, including database constraints. It’s up to you to determine what validations you want to include; you will be evaluated based on have more than one working validation in each of the following:

Table Constraints
Model Validations
Schema Validations

Task 2: Determine the Design
Entities
Exercise
id (integer, primary key)
name (string)
category (string)
equipment_needed (boolean)
Workout
id (integer, primary key)
date (date)
duration_minutes (integer)
notes (text)
WorkoutExercises (Join Table)
id (primary key)
workout_id (foreign key to Workout)
exercise_id (foreign key to Exercise)
reps (integer)
sets (integer)
duration_seconds (integer)
Relationships
A WorkoutExercise belongs to a Workout
A WorkoutExercise belongs to an Exercise
A Workout has many WorkoutExercises
An Exercise has many WorkoutExercises
A Workout has many Exercises through WorkoutExercises
An Exercise has many Workouts through WorkoutExercises

Required Endpoints
GET /workouts
List all workouts
GET /workouts/<id>
Stretch goal: include reps/sets/duration data from WorkoutExercises
Show a single workout with its associated exercises
POST /workouts
Create a workout
DELETE /workouts/<id>
Stretch goal: delete associated WorkoutExercises
Delete a workout
GET /exercises
List all exercises
GET /exercises/<id>
Show an exercise and associated workouts
POST /exercises
Create an exercise
DELETE /exercises/<id>
Stretch goal: delete associated WorkoutExercises
Delete an exercise
POST workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Add an exercise to a workout, including reps/sets/duration

Task 3: Develop the Code
Step 1: Set-Up Application Structure
Create GitHub repo with README and .gitignore (use Python template)
Create Pipfile (optionally from a requirements.txt file) with required packages (listed under Tools & Resources section)
Install packages
Create server/ directory with: app.py
from flask import Flask, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here

if __name__ == '__main__':
    app.run(port=5555, debug=True)
 models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here
 seed.py

#!/usr/bin/env python3

from app import app
from models import *

with app.app_context():

	# reset data and add new example data, committing to db 
 Commit your code with a meaningful commit message.

Step 2: Define Models
Exercise
id (integer, primary key)
name (string)
category (string)
equipment_needed (boolean)
Workout
id (integer, primary key)
date (date)
duration_minutes (integer)
notes (text)
WorkoutExercises (Join Table)
id (primary key)
workout_id (foreign key to Workout)
exercise_id (foreign key to Exercise)
reps (integer)
sets (integer)
duration_seconds (integer)
Commit your code with a meaningful commit message. It’s recommended to commit after building out each model individually, so you aren’t including too much new code in a single commit.

Step 3: Set Up Relationships
A WorkoutExercise belongs to a Workout
A WorkoutExercise belongs to an Exercise
A Workout has many WorkoutExercises
An Exercise has many WorkoutExercises
A Workout has many Exercises through WorkoutExercises
An Exercise has many Workouts through WorkoutExercises
Commit your code with a meaningful commit message.

Step 4: Create Table Constraints and Model Validations
Think about what constraints make sense. You need a minimum of 2 table constraints and 2 model validations to earn full points of the rubric.
Implement the table constraints.
Implement the model validations.
Commit your code with a meaningful commit message.

Step 5: Initialize Database and Migrate
flask db init
flask db migrate -m 'message about your migration here'
flask db upgrade head
Step 6: Create Seed File and Verify Relationships/Validations
Create seed file data.
Remember to clear out tables and create a few records for each table.
Run seed file.
Jump into flask shell to verify your relationships are set up properly and validations prevent bad data from being saved.
Rerun your seed file at any point to reset your database data.
Commit your code with a meaningful commit message.

Step 7: Create Endpoints
Scaffold out each endpoint. You’ll add functionality to these in step 10 after setting up serialization.

GET /workouts
List all workouts
GET /workouts/<id>
Stretch goal: include reps/sets/duration data from WorkoutExercises
Show a single workout with its associated exercises
POST /workouts
Create a workout
DELETE /workouts/<id>
Stretch goal: delete associated WorkoutExercises
Delete a workout
GET /exercises
List all exercises
GET /exercises/<id>
Show an exercise and associated workouts
POST /exercises
Create an exercise
DELETE /exercises/<id>
Stretch goal: delete associated WorkoutExercises
Delete an exercise
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Add an exercise to a workout, including reps/sets/duration
Commit your code with a meaningful commit message.

Step 8: Set up Schemas for Serialization and Deserialization
Use marshmallow to implement Schemas for each model

Commit your code with a meaningful commit message.

Step 9: Create Schema Validations
Think about what schema validations make sense. These can mirror your table constraints and model validations. You need a minimum of 2 schema validations to earn full points of the rubric.
Implement the schema validations.
Commit your code with a meaningful commit message.

Step 10: Edit Endpoints to use Schemas for Serialization and Deserialization
Use schemas to serialize and deserialize data, building out functionality for all endpoints

Commit your code with a meaningful commit message. It’s recommended to commit after building out each endpoint individually, so you aren’t including too much new code in a single commit.

Task 4: Test, Debug, and Refine Application
Ensure that the seed file executes without error or duplicating database data.
Use flask shell to determine all validations are working as expected.
Double check all API endpoints are working, error-free, and rendering the correct data as applicable.
Optionally, for extra practice and to take your application to the next level, create test suite for functionality (such as model validations or endpoint status codes).

Task 5: Document and Maintain
Step 1: Add Necessary Comments, Remove Unnecessary Comments
Include explanatory comments and/or docstrings on any unclear code.
Remove unnecessary, out dated, or unclear code comments.
Step 2: Create README with Required Information
Create a README.md with:

Project title
Project Description
Installation instructions (i.e. pipenv install, migrating and seeding the database, etc)
Run instructions (i.e. flask run)
List with descriptions of all endpoints the API has
Step 3: Final Commit and Push Git History
Ensure all code is pushed to GitHub and on the main branch.

Submission and Grading Criteria
Review the rubric below as a guide for how this lab will be graded.
Complete your assignment using your preferred IDE.
When you are ready, push your final script to GitHub. Your GitHub repository should include:
Full flask application, with all necessary files and code.
A functioning seed.py file to create example data for all models.
A README.md with the following:
Project title
Project Description
Installation instructions (i.e. pipenv install, migrating and seeding the database, etc)
Run instructions (i.e. flask run)
List with descriptions of all endpoints the API has
Pipfile with dependencies
Test files, if applicable
To submit your assignment, click on Start Assignment then share the link to your GitHub repo below. 
