from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Helper function for error responses
def create_error_response(message, status_code=400):
    return make_response(jsonify({'error': message}), status_code)

# Helper function for success responses
def create_success_response(data, status_code=200):
    return make_response(jsonify(data), status_code)

# WORKOUT ENDPOINTS
@app.route('/workouts', methods=['GET'])
def get_workouts():
    """List all workouts"""
    workouts = Workout.query.all()
    return create_success_response(workouts_schema.dump(workouts))

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    """Show a single workout with its associated exercises"""
    workout = Workout.query.get(id)
    if not workout:
        return create_error_response("Workout not found", 404)
    
    # Include workout exercises data for stretch goal
    workout_data = workout_schema.dump(workout)
    workout_data['workout_exercises'] = [
        {
            'id': we.id,
            'exercise': exercise_schema.dump(we.exercise),
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds
        }
        for we in workout.workout_exercises
    ]
    
    return create_success_response(workout_data)

@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a workout"""
    try:
        data = workout_schema.load(request.json)
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return create_success_response(workout_schema.dump(workout), 201)
    except ValidationError as e:
        return create_error_response(str(e.messages))
    except Exception as e:
        db.session.rollback()
        return create_error_response(str(e))

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout (stretch goal: delete associated WorkoutExercises)"""
    workout = Workout.query.get(id)
    if not workout:
        return create_error_response("Workout not found", 404)
    
    try:
        # Associated WorkoutExercises are deleted automatically due to cascade
        db.session.delete(workout)
        db.session.commit()
        return create_success_response({'message': 'Workout deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return create_error_response(str(e))

# EXERCISE ENDPOINTS
@app.route('/exercises', methods=['GET'])
def get_exercises():
    """List all exercises"""
    exercises = Exercise.query.all()
    return create_success_response(exercises_schema.dump(exercises))

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    """Show an exercise and associated workouts"""
    exercise = Exercise.query.get(id)
    if not exercise:
        return create_error_response("Exercise not found", 404)
    
    exercise_data = exercise_schema.dump(exercise)
    exercise_data['workouts'] = [
        {
            'id': workout.id,
            'date': workout.date.isoformat(),
            'duration_minutes': workout.duration_minutes,
            'notes': workout.notes
        }
        for workout in exercise.workouts
    ]
    
    return create_success_response(exercise_data)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create an exercise"""
    try:
        data = exercise_schema.load(request.json)
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return create_success_response(exercise_schema.dump(exercise), 201)
    except ValidationError as e:
        return create_error_response(str(e.messages))
    except Exception as e:
        db.session.rollback()
        return create_error_response(str(e))

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise (stretch goal: delete associated WorkoutExercises)"""
    exercise = Exercise.query.get(id)
    if not exercise:
        return create_error_response("Exercise not found", 404)
    
    try:
        # Associated WorkoutExercises are deleted automatically due to cascade
        db.session.delete(exercise)
        db.session.commit()
        return create_success_response({'message': 'Exercise deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return create_error_response(str(e))

# WORKOUT EXERCISE ENDPOINTS
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an exercise to a workout, including reps/sets/duration"""
    # Verify workout and exercise exist
    workout = Workout.query.get(workout_id)
    if not workout:
        return create_error_response("Workout not found", 404)
    
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return create_error_response("Exercise not found", 404)
    
    # Check if this combination already exists
    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id, 
        exercise_id=exercise_id
    ).first()
    if existing:
        return create_error_response("Exercise already added to this workout", 409)
    
    try:
        # Get additional data from request
        data = request.json or {}
        workout_exercise_data = {
            'workout_id': workout_id,
            'exercise_id': exercise_id,
            'reps': data.get('reps'),
            'sets': data.get('sets'),
            'duration_seconds': data.get('duration_seconds')
        }
        
        # Validate the data
        validated_data = workout_exercise_schema.load(workout_exercise_data)
        workout_exercise = WorkoutExercise(**validated_data)
        
        db.session.add(workout_exercise)
        db.session.commit()
        
        return create_success_response(workout_exercise_schema.dump(workout_exercise), 201)
    except ValidationError as e:
        return create_error_response(str(e.messages))
    except Exception as e:
        db.session.rollback()
        return create_error_response(str(e))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return create_error_response("Resource not found", 404)

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return create_error_response("Internal server error", 500)

if __name__ == '__main__':
    app.run(port=5555, debug=True)