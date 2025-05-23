#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta

def clear_data():
    """Clear all existing data from tables"""
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()
    print("Data cleared successfully!")

def seed_exercises():
    """Seed the database with sample exercises"""
    print("Seeding exercises...")
    
    exercises = [
        Exercise(name="push-ups", category="strength", equipment_needed=False),
        Exercise(name="squats", category="strength", equipment_needed=False),
        Exercise(name="deadlifts", category="strength", equipment_needed=True),
        Exercise(name="bench press", category="strength", equipment_needed=True),
        Exercise(name="running", category="cardio", equipment_needed=False),
        Exercise(name="cycling", category="cardio", equipment_needed=True),
        Exercise(name="yoga flow", category="flexibility", equipment_needed=False),
        Exercise(name="stretching", category="flexibility", equipment_needed=False),
        Exercise(name="basketball", category="sports", equipment_needed=True),
        Exercise(name="swimming", category="cardio", equipment_needed=False),
        Exercise(name="plank", category="strength", equipment_needed=False),
        Exercise(name="burpees", category="cardio", equipment_needed=False),
    ]
    
    for exercise in exercises:
        db.session.add(exercise)
    
    db.session.commit()
    print(f"Added {len(exercises)} exercises")
    return exercises

def seed_workouts():
    """Seed the database with sample workouts"""
    print("Seeding workouts...")
    
    today = date.today()
    workouts = [
        Workout(
            date=today - timedelta(days=7),
            duration_minutes=45,
            notes="Great upper body workout"
        ),
        Workout(
            date=today - timedelta(days=5),
            duration_minutes=60,
            notes="Leg day - felt strong"
        ),
        Workout(
            date=today - timedelta(days=3),
            duration_minutes=30,
            notes="Quick cardio session"
        ),
        Workout(
            date=today - timedelta(days=1),
            duration_minutes=50,
            notes="Full body workout"
        ),
        Workout(
            date=today,
            duration_minutes=35,
            notes="Morning flexibility routine"
        )
    ]
    
    for workout in workouts:
        db.session.add(workout)
    
    db.session.commit()
    print(f"Added {len(workouts)} workouts")
    return workouts

def seed_workout_exercises(exercises, workouts):
    """Seed the database with workout-exercise relationships"""
    print("Seeding workout exercises...")
    
    # Create a dictionary for easier exercise lookup
    exercise_dict = {exercise.name: exercise for exercise in exercises}
    
    # Print available exercises for debugging
    print(f"Available exercises: {list(exercise_dict.keys())}")
    
    # Get specific exercises for easier reference
    try:
        pushups = exercise_dict["Push-Ups"]  # Note the title case formatting from model validation
        squats = exercise_dict["Squats"]
        deadlifts = exercise_dict["Deadlifts"]
        bench_press = exercise_dict["Bench Press"]
        running = exercise_dict["Running"]
        cycling = exercise_dict["Cycling"]
        yoga = exercise_dict["Yoga Flow"]
        plank = exercise_dict["Plank"]
        burpees = exercise_dict["Burpees"]
    except KeyError as e:
        print(f"Could not find exercise: {e}")
        print("Available exercises:")
        for exercise in exercises:
            print(f"  - {exercise.name}")
        return
    
    workout_exercises = [
        # Workout 1 (Upper body) - 7 days ago
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=pushups.id, reps=15, sets=3),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=bench_press.id, reps=10, sets=4),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=plank.id, duration_seconds=60, sets=3),
        
        # Workout 2 (Leg day) - 5 days ago
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=squats.id, reps=20, sets=4),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=deadlifts.id, reps=8, sets=3),
        
        # Workout 3 (Cardio) - 3 days ago
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=running.id, duration_seconds=1800),  # 30 minutes
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=burpees.id, reps=10, sets=5),
        
        # Workout 4 (Full body) - 1 day ago
        WorkoutExercise(workout_id=workouts[3].id, exercise_id=pushups.id, reps=12, sets=3),
        WorkoutExercise(workout_id=workouts[3].id, exercise_id=squats.id, reps=15, sets=3),
        WorkoutExercise(workout_id=workouts[3].id, exercise_id=plank.id, duration_seconds=45, sets=3),
        WorkoutExercise(workout_id=workouts[3].id, exercise_id=cycling.id, duration_seconds=900),  # 15 minutes
        
        # Workout 5 (Flexibility) - Today
        WorkoutExercise(workout_id=workouts[4].id, exercise_id=yoga.id, duration_seconds=2100),  # 35 minutes
    ]
    
    for we in workout_exercises:
        db.session.add(we)
    
    db.session.commit()
    print(f"Added {len(workout_exercises)} workout-exercise relationships")

def main():
    """Main seeding function"""
    with app.app_context():
        print("Starting database seeding...")
        
        # Clear existing data
        clear_data()
        
        # Seed new data
        exercises = seed_exercises()
        workouts = seed_workouts()
        seed_workout_exercises(exercises, workouts)
        
        print("\nDatabase seeding completed successfully!")
        print(f"Total exercises: {Exercise.query.count()}")
        print(f"Total workouts: {Workout.query.count()}")
        print(f"Total workout-exercise relationships: {WorkoutExercise.query.count()}")

if __name__ == '__main__':
    main()